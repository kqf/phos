from spectrum.pipeline import TransformerBase
from spectrum.pipeline import Pipeline
from spectrum.pipeline import ParallelPipeline
from spectrum.pipeline import ReduceArgumentPipeline
from spectrum.efficiency import Efficiency
from spectrum.broot import BROOT as br
from spectrum.options import CompositeEfficiencyOptions

from vault.datavault import DataVault
from spectrum.tools.deviation import MaxDeviationVector


class NonlinearityUncertaintyOptions(object):

    def __init__(self, particle="#pi^{0}", nbins=11, n_ranges=2):
        super(NonlinearityUncertaintyOptions, self).__init__()
        self.nbins = nbins
        self.eff = CompositeEfficiencyOptions(particle)


def chi2_func(hist1, hist2, loggs):
    return br.chi2ndf(hist1, hist2)


class NonlinearityUncertainty(TransformerBase):
    def __init__(self, options=NonlinearityUncertaintyOptions(),
                 chi2_=chi2_func,
                 plot=True):
        super(NonlinearityUncertainty, self).__init__()
        main = Pipeline([
            ('efficiency_main', Efficiency(options.eff, plot))
        ])

        mc = ParallelPipeline([
            ("efficiency_" + str(i), Efficiency(options.eff, plot))
            for i in range(options.nbins ** 2)
        ])

        ratio = ReduceArgumentPipeline(mc, main,
                                       lambda x, y, loggs=None: br.ratio(x, y))
        self.pipeline = Pipeline([
            ("ratios", ratio),
            ("deviation", MaxDeviationVector())
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

    return (efficiency_inputs, spmc)
