import spectrum.broot as br
from joblib import Memory
from spectrum.pipeline import RebinTransformer
from spectrum.pipeline import Pipeline
from spectrum.pipeline import FunctionTransformer
from spectrum.efficiency import Efficiency
from spectrum.options import CompositeEfficiencyOptions, Options
from spectrum.output import open_loggs
from spectrum.pipeline import ParallelPipeline, TransformerBase
from spectrum.plotter import plot
from vault.datavault import DataVault


class NonlinearityUncertaintyOptions(object):

    def __init__(self, particle="#pi^{0}", nbins=9, n_ranges=2):
        super(NonlinearityUncertaintyOptions, self).__init__()
        self.nbins = nbins
        self.eff = CompositeEfficiencyOptions("#pi^{0}")
        self.edges = None
        if particle != "#pi^{0}":
            self.edges = Options(particle=particle).pt.ptedges
        self.particle = particle


memory = Memory(".joblib-cachedir", verbose=0)


# TODO: Handle loggs
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


def visualise(effs, loggs, stop=False):
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

    uncert, rms, mean = br.systematic_deviation(effs)
    uncert.logy = False
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


def form_histnames(nbins=4):
    histnames = sum([
        [
            "hMassPt_{}_{}".format(i, j),
            "hMixMassPt_{}_{}".format(i, j),
        ]
        for j in range(nbins)
        for i in range(nbins)
    ], [])
    return histnames


# TODO: Add Generated Histogram to the nonlinearity scan selection
#
def nonlinearity_scan_data(nbins, prod, eff_prod="PhysEff"):
    histnames = form_histnames(nbins)
    low = DataVault().input(prod, "low", inputs=histnames)
    high = DataVault().input(prod, "high", inputs=histnames)

    efficiency_inputs = (
        DataVault().input(prod, "low", "PhysEff"),
        DataVault().input(prod, "high", "PhysEff")
    )

    spmc = [(l, h) for l, h in zip(
        low.read_multiple(single=efficiency_inputs[0]),
        high.read_multiple(single=efficiency_inputs[1])
    )]

    return spmc
