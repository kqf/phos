from spectrum.pipeline import TransformerBase
from spectrum.options import CompositeCorrectedYieldOptions, Options
from spectrum.pipeline import ReducePipeline
from spectrum.pipeline import ParallelPipeline
from spectrum.pipeline import Pipeline
from spectrum.pipeline import RebinTransformer
from spectrum.corrected_yield import CorrectedYield
from spectrum.broot import BROOT as br
from spectrum.comparator import Comparator
from spectrum.tools.unityfit import UnityFitTransformer
from spectrum.tools.feeddown import data_feeddown
from vault.datavault import DataVault


def cyield_data(particle, cut):
    mc_production = "single {}".format(particle)
    data_input = (
        DataVault().input(
            "data",
            listname="Phys{}".format(cut),
            histname="MassPtSM0"),
        data_feeddown(particle != "#pi^{0}"),
    )
    mc_inputs = (
        DataVault().input(
            mc_production, "low",
            listname="PhysEff{}".format(cut),
            # histname="MassPtSM0"
        ),
        DataVault().input(
            mc_production, "high",
            listname="PhysEff{}".format(cut),
            # histname="MassPtSM0"
        ),
    )
    return data_input, mc_inputs


def acceptance_data(particle="#pi^{0}"):
    return (
        cyield_data("#pi^{0}", cut=1),
        cyield_data("#pi^{0}", cut=2),
        # cyield_data("#pi^{0}", cut=3),
        # cyield_data("#pi^{0}", cut=4),
    )


class AcceptanceOptions(object):
    title = "Acceptance uncertainty; p_{T}, GeV/c; Relateive error, %"

    def __init__(self, particle="#pi^{0}"):
        super(AcceptanceOptions, self).__init__()
        self.cyield = CompositeCorrectedYieldOptions(particle="#pi^{0}")
        self.fit_range = (1, 10)
        self.edges = None
        if particle == "#pi^{0}":
            return
        self.edges = Options(particle="#eta").pt.ptedges


class MaxUnityHistogram(object):
    def transform(self, hists, loggs):
        return max(hists, key=lambda x: x.GetBinContent(1))


class SaveImagesTransformer(object):

    def transform(self, hists, loggs):
        Comparator().compare(hists, loggs=loggs)
        return hists


class RemoveErrors(object):

    def transform(self, hist, loggs):
        for i in br.range(hist):
            hist.SetBinError(i, 0)
        return hist


class Acceptance(TransformerBase):
    def __init__(self, options, plot=False):
        super(Acceptance, self).__init__(plot)
        unities = ReducePipeline(
            ParallelPipeline([
                ("no cut", CorrectedYield(options.cyield)),
                ("min. dist. 1 cell", CorrectedYield(options.cyield)),
                # ("min. dist. 2 cells", CorrectedYield(options.cyield)),
                # ("min. dist. 3 cells", CorrectedYield(options.cyield)),
            ]),
            self.ratio
        )

        self.pipeline = Pipeline([
            ("unities", unities),
            ("fit", UnityFitTransformer(options.title, options.fit_range)),
            ("max", MaxUnityHistogram()),
            ("final", RemoveErrors()),
            ("rebin", RebinTransformer(True, options.edges)),
        ])

    def ratio(self, spectrums, loggs):
        average = br.average(spectrums, "averaged yield")
        # Comparator().compare(spectrums)
        diff = Comparator(stop=self.plot, oname="yield_deviation_from_average")
        # uncert, rms, mean = br.systematic_deviation(spectrums)
        # uncert.logy = False
        # loggs.update({"uncertainty": uncert})
        # loggs.update({"rms": rms})
        # loggs.update({"mean": mean})
        # return uncert

        diff.compare_ratios(spectrums, average, loggs=loggs)
        ratios = [br.ratio(average, s) for s in spectrums]
        for r in ratios:
            r.logy = False
        diff.compare(ratios)
        #     "Systematic uncertanity from yield extraction (RMS/mean)")
        # diff = Comparator(stop=self.plot,
        #                   oname="syst-error-yield-extraction")
        # diff.compare(uncert)
        return ratios
