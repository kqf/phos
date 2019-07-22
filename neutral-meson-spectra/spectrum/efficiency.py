from pipeline import TransformerBase
from options import EfficiencyOptions, CompositeEfficiencyOptions
from .input import SingleHistInput
from analysis import Analysis
from pipeline import Pipeline, HistogramSelector
from pipeline import OutputDecorator
from pipeline import ReducePipeline, ParallelPipeline, HistogramScaler
from pipeline import ComparePipeline
from pipeline import RebinTransformer
from broot import BROOT as br
from processing import RangeEstimator

# NB: This test is to compare different efficiencies
#     estimated from different productions
#


class SimpleEfficiency(TransformerBase):

    def __init__(self, options, plot=False):
        super(SimpleEfficiency, self).__init__(plot)
        scaled_ryield = Pipeline([
            ("ReconstructMesons", Analysis(options.analysis)),
            ("NumberOfMesons", HistogramSelector("nmesons")),
            ("ScaleForAcceptance", HistogramScaler(options.scale))
        ])

        generated = Pipeline([
            ("raw", SingleHistInput(options.genname)),
            ("rebinned", RebinTransformer(
                edges=options.analysis.pt.ptedges,
                width=True)),
        ])

        efficiency = ComparePipeline([
            ("raw-yield", scaled_ryield),
            ("generated", generated),
        ], ratio="B")

        self.pipeline = Pipeline([
            ('efficiency', efficiency),
            ('decorate', OutputDecorator(*options.decorate))
        ])

    def transform(self, data, loggs):
        # NB: Compare pipeline takes the intput two times
        return super(SimpleEfficiency, self).transform(
            (data, data), loggs=loggs)


class PeakPositionWidthEstimator(TransformerBase):
    def __init__(self, options, plot=False):
        super(PeakPositionWidthEstimator, self).__init__(plot)
        self.options = options
        self.pipeline = Analysis(options.analysis)
        name, option = options.analysis.steps[0]
        self.restimator = RangeEstimator(option.calibration)

    def _estimate(self, data, loggs):
        output = self.pipeline.transform(data, loggs)
        pt_range = data[0].pt_range[0], data[1].pt_range[1]
        output.mass.GetXaxis().SetRangeUser(*pt_range)
        output.width.GetXaxis().SetRangeUser(*pt_range)

        massf = self.restimator.mass.steps[0][1]._fit(output.mass).fitf
        widthf = self.restimator.width.steps[0][1]._fit(output.width).fitf
        return output.mass, massf, output.width, widthf

    def transform(self, data, loggs):
        mass, massf, width, widthf = self._estimate(data, loggs)
        mass_pars, _ = br.pars(massf)
        width_pars, _ = br.pars(widthf)

        for option in self.options.suboptions:
            option.analysis.calibration.mass.pars = mass_pars
            option.analysis.calibration.mass.fit = False

            option.analysis.calibration.width.pars = width_pars
            option.analysis.calibration.width.fit = False

        loggs.update({"mass": mass, "width": width})
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
        return "{0} < p_{{T}} < {1} GeV/c".format(*ranges)

    def _reduce_function(self, options):
        if options.reduce_function != "standard":
            return options.reduce_function
        return lambda x, loggs: br.sum_trimm(x, options.mergeranges)


class Efficiency(TransformerBase):

    _efficiency_types = {
        EfficiencyOptions: SimpleEfficiency,
        CompositeEfficiencyOptions: CompositeEfficiency
    }

    def __init__(self, options=EfficiencyOptions(), plot=False):
        super(Efficiency, self).__init__(plot)
        EfficiencyType = self._efficiency_types.get(type(options))
        self.pipeline = EfficiencyType(options, plot)
