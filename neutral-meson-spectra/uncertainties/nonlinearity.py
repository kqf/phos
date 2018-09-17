import ROOT
from spectrum.transformer import TransformerBase
from spectrum.pipeline import Pipeline
from spectrum.pipeline import ParallelPipeline
from spectrum.pipeline import ReduceArgumentPipeline
from spectrum.efficiency import Efficiency
from spectrum.broot import BROOT as br

from uncertainties.deviation import MaxDeviationVector


class Nonlinearity(TransformerBase):
    def __init__(self, options, chi2_=br.chi2ndf, plot=True):
        super(Nonlinearity, self).__init__()
        main = Pipeline([
            ('efficiency_main', Efficiency(options.eff, plot))
        ])

        mc = ParallelPipeline([
            ("efficiency_" + str(i), Efficiency(options.eff, plot))
            for i in range(options.nbins ** 2)
        ])

        ratio = ReduceArgumentPipeline(mc, main, br.ratio)
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
