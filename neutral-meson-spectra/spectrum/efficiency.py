#!/usr/bin/python

from transformer import TransformerBase
from options import EfficiencyOptions, CompositeEfficiencyOptions
from .input import SingleHistInput
from analysis import Analysis
from pipeline import Pipeline, RatioUnion, HistogramSelector
from pipeline import OutputDecorator
from pipeline import ReducePipeline, ParallelPipeline, HistogramScaler
from broot import BROOT as br
from processing import RangeEstimator

# NB: This test is to compare different efficiencies
#     estimated from different productions
#


# TODO: Rewrite RatioUnion to accept list of estimators
#       add named steps, etc
#

class SimpleEfficiency(TransformerBase):

    def __init__(self, options, plot=False):
        super(SimpleEfficiency, self).__init__(plot)
        efficiency = RatioUnion(
            Pipeline([
                ("ReconstructMesons", Analysis(options.analysis)),
                ("NumberOfMesons", HistogramSelector("nmesons")),
                ("ScaleForAcceptance", HistogramScaler(options.scale))
            ]),
            SingleHistInput(options.genname)
        )
        self.pipeline = Pipeline([
            ('efficiency', efficiency),
            ('decorate', OutputDecorator(*options.decorate))
        ])


class PeakPositionWidthEstimator(TransformerBase):
    def __init__(self, options, plot=False):
        super(PeakPositionWidthEstimator, self).__init__(plot)
        self.options = options
        self.pipeline = Analysis(options.analysis)
        name, option = options.analysis.steps[0]
        self.restimator = RangeEstimator(option.spectrum)

    def _estimate(self, data, loggs):
        output = self.pipeline.transform(data, loggs)

        massf = self.restimator.fit_mass(output.mass)
        widthf = self.restimator.fit_sigma(output.width)
        return output.mass, massf, output.width, widthf

    def transform(self, data, loggs):
        mass, massf, width, widthf = self._estimate(data, loggs)
        mass_pars, _ = br.pars(massf)
        width_pars, _ = br.pars(widthf)

        for option in self.options.suboptions:
            option.analysis.spectrum.mass_pars = mass_pars
            option.analysis.spectrum.width_pars = width_pars
            option.analysis.spectrum.fit_mass_width = False

        loggs.update(
            "composite_range_estimator",
            [mass, width],
            mergable=True)
        return data  # NB: Don't change the data


class CompositeEfficiency(TransformerBase):

    def __init__(self, options, plot=False):
        super(CompositeEfficiency, self).__init__(plot)
        efficiency = ReducePipeline(
            ParallelPipeline([
                (self._stepname(ranges), Efficiency(opt, plot))
                for (opt, ranges) in zip(options.suboptions,
                                         options.mergeranges)
            ]),
            self._reduce_function(options)
        )
        self.pipeline = Pipeline([
            ("preliminary fit", PeakPositionWidthEstimator(options)),
            ("efficiency", efficiency)
        ])

    def _stepname(self, ranges):
        return "{0} < p_{T} < {1} GeV/c".format(*ranges, T='{T}')

    def _reduce_function(self, options):
        if options.reduce_function != "standard":
            return options.reduce_function
        return lambda x: br.sum_trimm(x, options.mergeranges)


class Efficiency(TransformerBase):

    _efficiency_types = {
        EfficiencyOptions: SimpleEfficiency,
        CompositeEfficiencyOptions: CompositeEfficiency
    }

    def __init__(self, options=EfficiencyOptions(), plot=False):
        super(Efficiency, self).__init__(plot)
        EfficiencyType = self._efficiency_types.get(type(options))
        efficiency = EfficiencyType(options, plot)
        self.pipeline = efficiency.pipeline
