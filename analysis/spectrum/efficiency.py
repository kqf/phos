from spectrum.pipeline import TransformerBase
from spectrum.options import EfficiencyOptions, CompositeEfficiencyOptions
from spectrum.pipeline import SingleHistReader
from spectrum.analysis import Analysis
from spectrum.pipeline import Pipeline, HistogramSelector
from spectrum.pipeline import OutputDecorator
from spectrum.pipeline import ReducePipeline, ParallelPipeline, HistogramScaler
from spectrum.pipeline import ComparePipeline
from spectrum.pipeline import RebinTransformer
import spectrum.broot as br
from spectrum.processing import PtFitter
from spectrum.vault import DataVault

# NB: This test is to compare different efficiencies
#     estimated from different productions
#


def simple_efficiency_data(
        particle="#pi^{0}",
        prod="pythia8",
        listname="PhysEff",
        histname="hPt_{0}_primary_standard",
):
    histname = histname.format(particle)
    return (
        DataVault().input(prod, listname=listname),
        DataVault().input(prod, listname=listname, histname=histname),
    )


def efficiency_data(
    particle="#pi^{0}",
    prod=None,
    listname="PhysEff",
    histname="hPt_{0}_primary_standard",
):
    histname = histname.format(particle)
    prod = prod or "single {}".format(particle)
    return (
        (
            DataVault().input(prod, "low", listname),
            DataVault().input(prod, "low", listname, histname=histname),
        ),
        (
            DataVault().input(prod, "high", listname),
            DataVault().input(prod, "high", listname, histname=histname),
        )
    )


class SimpleEfficiency(TransformerBase):

    def __init__(self, options, plot=False):
        super(SimpleEfficiency, self).__init__(plot)
        reconstructed = Pipeline([
            ("analysis", Analysis(options.analysis)),
            ("nmesons", HistogramSelector("nmesons")),
            ("scale-for-acceptance", HistogramScaler(options.scale))
        ])

        generated = Pipeline([
            ("raw", SingleHistReader()),
            ("rebinned", RebinTransformer(
                normalized=False,
                edges=options.analysis.pt.ptedges,
            )),
        ])

        efficiency = ComparePipeline([
            ("reconstructed", reconstructed),
            ("generated", generated),
        ], ratio="B")

        self.pipeline = Pipeline([
            ('efficiency', efficiency),
            ('decorate', OutputDecorator(**options.decorate))
        ])


class PeakPositionWidthEstimator(TransformerBase):
    def __init__(self, options, plot=False):
        super(PeakPositionWidthEstimator, self).__init__(plot)
        self.options = options
        self.pipeline = Analysis(options.analysis)
        name, option = options.analysis.steps[0]
        self.mass = PtFitter(col=None, err=None, out_col=None,
                             options=option.calibration.mass)
        self.width = PtFitter(col=None, err=None, out_col=None,
                              options=option.calibration.width)

    def _estimate(self, data, loggs):
        data = data[0][0], data[1][0]
        output = self.pipeline.transform(data, loggs)
        pt_range = data[0].pt_range[0], data[1].pt_range[1]
        output.mass.GetXaxis().SetRangeUser(*pt_range)
        output.width.GetXaxis().SetRangeUser(*pt_range)

        massf = self.mass._fit(output.mass)
        widthf = self.width._fit(output.width)
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
        return "{} < p_{{T}} < {} GeV/#it{{c}}".format(*ranges)

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
