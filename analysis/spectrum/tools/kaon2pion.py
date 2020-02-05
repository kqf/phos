import spectrum.broot as br
from spectrum.pipeline import SingleHistReader
from spectrum.pipeline import TransformerBase
from spectrum.pipeline import ReducePipeline, ParallelPipeline
from spectrum.pipeline import ComparePipeline


class HistSum(TransformerBase):
    def __init__(self):
        super(HistSum, self).__init__()
        self.pipeline = ReducePipeline(
            ParallelPipeline([
                ("kaons", SingleHistReader()),
                ("pions", SingleHistReader()),

            ]),
            lambda x, loggs: br.hsum(x)
        )


class DoubleK2POptions(object):
    def __init__(self, reduce_func):
        self.reduce_func = reduce_func


class KaonToPionRatioMC(TransformerBase):
    def __init__(self, plot=False):
        super(KaonToPionRatioMC, self).__init__()
        self.pipeline = ComparePipeline([
            ("kaons", HistSum()),
            ("pions", HistSum())
        ], plot)


# NB: Real Data distributions are stored in
#     separate files produced by ALCIE
class KaonToPionRatioData(TransformerBase):
    def __init__(self, plot=False):
        super(KaonToPionRatioData, self).__init__()
        self.pipeline = ComparePipeline([
            ("kaons", SingleHistReader()),
            ("pions", SingleHistReader()),
        ], plot)


class KaonToPionDoubleRatio(TransformerBase):
    def __init__(self, options, plot=False):
        super(KaonToPionDoubleRatio, self).__init__()
        self.pipeline = ReducePipeline(
            ParallelPipeline([
                ("data", KaonToPionRatioData()),
                ("mc", KaonToPionRatioMC()),
            ]),
            lambda x, loggs: options.reduce_func(x, loggs, stop=plot)
        )
