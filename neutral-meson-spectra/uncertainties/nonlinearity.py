import ROOT
from spectrum.analysis import Analysis
from spectrum.transformer import TransformerBase
from spectrum.pipeline import Pipeline
from spectrum.pipeline import ParallelPipeline
from spectrum.pipeline import HistogramSelector
from spectrum.pipeline import ReducePipeline
from spectrum.pipeline import HistogramScaler
from spectrum.broot import BROOT as br


class Nonlinearity(TransformerBase):
    def __init__(self, options, chi2_=br.chi2ndf, plot=True):
        super(Nonlinearity, self).__init__()
        mass = Pipeline([
            ("reconstruction", Analysis(options.analysis, plot)),
            ("mass", HistogramSelector("mass")),
            ("scale", HistogramScaler(factor=options.factor)),
        ])

        masses_mc = ParallelPipeline([
            ("mass" + str(i), mass)
            for i in range(options.nbins ** 2)
        ])

        self.pipeline = ReducePipeline(masses_mc, br.sum)


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
