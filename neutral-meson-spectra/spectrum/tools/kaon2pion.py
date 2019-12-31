from collections import namedtuple
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
                ("kaons", SingleHistReader(nevents=1)),
                ("pions", SingleHistReader(nevents=1)),

            ]),
            lambda x, loggs: br.hsum(x)
        )


K2POptions = namedtuple("K2POptions", ["pions", "kaons"])
DoubleK2POptions = namedtuple("DoubleK2POptions", ["data", "mc",
                                                   "reduce_func"])


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
            ("kaons", SingleHistReader(nevents=1)),
            ("pions", SingleHistReader(nevents=1)),
        ], plot)


class KaonToPionDoubleRatio(TransformerBase):
    def __init__(self, options, plot=False):
        super(KaonToPionDoubleRatio, self).__init__()
        self.pipeline = ReducePipeline(
            ParallelPipeline([
                ("data", KaonToPionRatioData()),
                ("mc", KaonToPionRatioMC()),
            ]),
            options.reduce_func
        )
