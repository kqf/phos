import spectrum.broot as br
from joblib import Memory
from spectrum.pipeline import RebinTransformer
from spectrum.pipeline import Pipeline, HistogramSelector
from spectrum.pipeline import FunctionTransformer
from spectrum.efficiency import Efficiency
from spectrum.options import CompositeEfficiencyOptions, Options
from spectrum.options import CompositeOptions
from spectrum.output import open_loggs
from spectrum.pipeline import ParallelPipeline, TransformerBase
from spectrum.plotter import plot
from spectrum.analysis import Analysis
from spectrum.vault import DataVault


class NonlinearityUncertaintyOptions(object):

    def __init__(self, particle="#pi^{0}", nbins=9, n_ranges=2):
        super(NonlinearityUncertaintyOptions, self).__init__()
        self.nbins = nbins
        self.eff = CompositeEfficiencyOptions("#pi^{0}", genlist="PhysEff")
        self.edges = None
        if particle != "#pi^{0}":
            self.edges = Options(particle=particle).pt.ptedges
        self.particle = particle


memory = Memory(".joblib-cachedir", verbose=0)


@memory.cache()
def _eff(data, plot=False):
    options = NonlinearityUncertaintyOptions()
    mc = ParallelPipeline([
        ("efficiency_" + str(i), Efficiency(options.eff, plot))
        for i in range(options.nbins ** 2)
    ], disable=False)

    with open_loggs() as loggs:
        output = mc.transform(data, loggs)
    return output


@memory.cache()
def _masses(prod):
    def mass():
        options = CompositeOptions(particle="#pi^{0}")
        return Pipeline([
            ("Analysis", Analysis(options)),
            ("mass", HistogramSelector("mass")),
        ])
    nbins = NonlinearityUncertaintyOptions().nbins
    data = nonlinearity_scan_data(nbins, prod)
    mc = ParallelPipeline([
        ("mass_" + str(i), mass())
        for i in range(nbins ** 2)
    ], disable=False)

    with open_loggs() as loggs:
        output = mc.transform(data, loggs)
    return output


def visualise(effs, loggs, stop=False):
    # for i, eff in enumerate(effs):
    #     eff.Scale(1 + 0.001 * i)
    plot(
        effs,
        xtitle="p_{T} (GeV/#it{c})",
        csize=(96, 128),
        legend_pos=None,
        oname="results/systematics/nonlinearity/efficiencies.pdf",
        stop=stop,
        more_logs=False,
        colors='coolwarm',
        yoffset=1.6,
        ltext_size=0.015
    )

    average = br.average(effs, "averaged yield")
    average.GetYaxis().SetTitle("average")
    ratios = list(map(lambda x: br.ratio(x, average), effs))
    for i, r in enumerate(ratios):
        if any(br.bins(r).contents < 0.94):
            print("The problematic index: ", i)
    plot(
        list(map(lambda x: br.ratio(x, average), effs)),
        logy=False,
        xtitle="p_{T} (GeV/#it{c})",
        csize=(96, 128),
        legend_pos=None,
        oname="results/systematics/nonlinearity/ratios.pdf",
        stop=stop,
        colors='coolwarm',
        more_logs=False,
        yoffset=1.6,
        ltext_size=0.015
    )

    uncert, rms, mean = br.maximum_deviation(effs)
    loggs.update({"uncertainty": uncert})
    loggs.update({"rms": rms})
    loggs.update({"mean": mean})
    return uncert


class NonlinearityUncertainty(TransformerBase):
    def __init__(self, options=NonlinearityUncertaintyOptions(),
                 plot=True):
        super(NonlinearityUncertainty, self).__init__()
        self.options = options
        self.pipeline = Pipeline([
            ("effs", FunctionTransformer(_eff, no_loggs=True, plot=plot)),
            ("visualise", FunctionTransformer(visualise, stop=plot)),
            ("rebin", RebinTransformer(True, options.edges)),
        ])


def nonlinearity_scan_data(nbins, prod, eff_prod="PhysEff"):
    spmc = []
    genname = "hPt_#pi^{0}_primary_standard"
    for i in range(nbins):
        for j in range(nbins):
            histname = "MassPt_{}_{}".format(i, j)
            selection = (
                (
                    DataVault().input(prod, "low", histname=histname),
                    DataVault().input(prod, "low", "PhysEff",
                                      histname=genname),
                ),
                (
                    DataVault().input(prod, "high", histname=histname),
                    DataVault().input(prod, "high", "PhysEff",
                                      histname=genname),
                )
            )
            spmc.append(selection)
    return spmc
