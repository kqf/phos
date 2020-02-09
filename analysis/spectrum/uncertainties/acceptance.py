import spectrum.broot as br
from spectrum.pipeline import TransformerBase
from spectrum.options import CompositeCorrectedYieldOptions, Options
from spectrum.pipeline import ReducePipeline
from spectrum.pipeline import ParallelPipeline
from spectrum.pipeline import Pipeline
from spectrum.pipeline import RebinTransformer
from spectrum.cyield import CorrectedYield, cyield_data
from spectrum.comparator import Comparator
from spectrum.tools.unityfit import UnityFitTransformer
from spectrum.plotter import plot


def acceptance_data(particle="#pi^{0}"):
    return (
        cyield_data("#pi^{0}", listname_eff="PhysEff1"),
        cyield_data("#pi^{0}", listname_eff="PhysEff2"),
        # cyield_data("#pi^{0}", listname_eff="PhysEff3"),
        # cyield_data("#pi^{0}", listname_eff="PhysEff4"),
    )


class AcceptanceOptions(object):
    title = "Acceptance ; #it{p}_{T} (GeV/#it{c}); rel. sys. error"

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
            xtitle="#it{p}_{T} (GeV/#it{c})",
            csize=(96, 128),
            legend_pos=(0.5, 0.7, 0.7, 0.85),
            oname="images/systematics/acceptance/yields.pdf",
            stop=self.plot,
            more_logs=False,
            yoffset=1.6,
            ltitle="#pi^{0} #rightarrow #gamma #gamma",
        )
        average = br.average(spectrums, "averaged yield")
        average.SetTitle("average")
        ratios = [br.ratio(s, average) for s in spectrums]
        for ratio in ratios:
            for i in br.hrange(ratio):
                ratio.SetBinError(i, ratio.GetBinError(i))

        plot(
            ratios,
            logy=False,
            xtitle="#it{p}_{T} (GeV/#it{c})",
            ytitle="{} / average".format(spectrums[0].GetYaxis().GetTitle()),
            csize=(96, 128),
            legend_pos=(0.5, 0.7, 0.7, 0.85),
            oname="images/systematics/acceptance/ratios.pdf",
            stop=self.plot,
            more_logs=False,
            yoffset=1.8,
            ltitle="#pi^{0} #rightarrow #gamma #gamma",
        )
        return ratios
