import six
from joblib import Memory

from spectrum.pipeline import TransformerBase
from spectrum.pipeline import Pipeline
from spectrum.pipeline import ParallelPipeline
from spectrum.pipeline import ReduceArgumentPipeline
from spectrum.pipeline import RebinTransformer
from spectrum.efficiency import Efficiency
import spectrum.broot as br
from spectrum.options import CompositeEfficiencyOptions, Options
from spectrum.output import open_loggs

from vault.datavault import DataVault
from spectrum.plotter import plot
import spectrum.sutils as su


class NonlinearityUncertaintyOptions(object):

    def __init__(self, particle="#pi^{0}", nbins=9, n_ranges=2):
        super(NonlinearityUncertaintyOptions, self).__init__()
        self.nbins = nbins
        self.eff = CompositeEfficiencyOptions("#pi^{0}")
        self.edges = None
        if particle != "#pi^{0}":
            self.edges = Options(particle=particle).pt.ptedges
        self.particle = particle


def chi2_func(hist1, hist2, loggs):
    return br.chi2ndf(hist1, hist2)


memory = Memory(".joblib-cachedir", verbose=0)


@memory.cache()
def efficiencies(data, particle, plot=False):
    options = NonlinearityUncertaintyOptions(particle=particle)
    mc = ParallelPipeline([
        ("efficiency_" + str(i), Efficiency(options.eff, plot))
        for i in range(options.nbins ** 2)
    ], disable=False)
    with open_loggs() as loggs:
        output = mc.transform(data, loggs)
    return output


class NonlinearityUncertainty(TransformerBase):
    def __init__(self, options=NonlinearityUncertaintyOptions(),
                 chi2_=chi2_func,
                 plot=True):
        super(NonlinearityUncertainty, self).__init__()
        self.options = options

    def transform(self, data, loggs):
        print(self.options.particle)
        effs = efficiencies(data[1], self.options.particle)
        plot(
            effs,
            xtitle="p_{T} (GeV/#it{c})",
            csize=(96, 128),
            legend_pos=None,
            oname="results/systematics/yields/spectra-{}.pdf".format(
                su.spell(self.options.particle)),
            stop=self.plot,
            more_logs=False,
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
            oname="results/systematics/yields/ratios-{}.pdf".format(
                su.spell(self.options.particle)),
            stop=self.plot,
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

    return (efficiency_inputs, spmc)
