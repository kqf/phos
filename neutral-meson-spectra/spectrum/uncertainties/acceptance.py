from spectrum.pipeline import TransformerBase
from spectrum.options import CompositeCorrectedYieldOptions, Options
from spectrum.pipeline import ReducePipeline
from spectrum.pipeline import ParallelPipeline
from spectrum.pipeline import Pipeline
from spectrum.pipeline import RebinTransformer
from spectrum.corrected_yield import CorrectedYield
import spectrum.broot as br
from spectrum.comparator import Comparator
from spectrum.tools.unityfit import UnityFitTransformer
from spectrum.tools.feeddown import data_feeddown
from vault.datavault import DataVault
from spectrum.plotter import plot


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
    title = "Acceptance uncertainty; p_{T} (GeV)/c; Relateive error, %"

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
        for i in br.hrange(hist):
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
        for i, r in enumerate(spectrums):
            r.SetTitle("dist. to a bad cell > {} cm".format(i + 1))

        plot(
            spectrums,
            xtitle="p_{T} (GeV/#it{c})",
            csize=(96, 128),
            legend_pos=(0.5, 0.7, 0.7, 0.85),
            oname="results/systematics/acceptance/yields.pdf",
            stop=self.plot,
            more_logs=False,
            yoffset=1.6,
        )
        average = br.average(spectrums, "averaged yield")
        average.SetTitle("average")
        ratios = [br.ratio(s, average, "B") for s in spectrums]
        plot(
            ratios,
            logy=False,
            xtitle="p_{T} (GeV/#it{c})",
            ytitle="{} / average".format(spectrums[0].GetYaxis().GetTitle()),
            csize=(96, 128),
            legend_pos=(0.5, 0.7, 0.7, 0.85),
            oname="results/systematics/acceptance/ratios.pdf",
            stop=self.plot,
            more_logs=False,
            yoffset=1.8,
        )
        return ratios
