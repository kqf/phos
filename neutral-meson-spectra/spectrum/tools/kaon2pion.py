from collections import namedtuple
import spectrum.broot as br
from spectrum.input import SingleHistInput
from spectrum.pipeline import TransformerBase
from spectrum.pipeline import ReducePipeline, ParallelPipeline
from spectrum.pipeline import ComparePipeline
from spectrum.pipeline import Pipeline
from spectrum.comparator import Comparator


class HistSum(TransformerBase):
    def __init__(self, names):
        super(HistSum, self).__init__()
        self.pipeline = ReducePipeline(
            ParallelPipeline([
                (name, SingleHistInput(name)) for name in names
            ]),
            lambda x, loggs: br.hsum(x)
        )


K2POptions = namedtuple("K2POptions", ["pions", "kaons"])
DoubleK2POptions = namedtuple("DoubleK2POptions", ["data", "mc", "fitfunc"])


class KaonToPionRatioMC(TransformerBase):
    def __init__(self, options, plot=False):
        super(KaonToPionRatioMC, self).__init__()
        self.pipeline = ComparePipeline([
            ("kaons", HistSum(options.kaons)),
            ("pions", HistSum(options.pions))
        ], plot)


# NB: Real Data distributions are stored in
#     separate files produced by ALCIE
class KaonToPionRatioData(TransformerBase):
    def __init__(self, options, plot=False):
        super(KaonToPionRatioData, self).__init__()
        self.pipeline = ComparePipeline([
            ("kaons", SingleHistInput(options.kaons)),
            ("pions", SingleHistInput(options.pions)),
        ], plot)


def rebin_compare(inputs, loggs):
    data, mc = inputs
    title = """
    Charged kaon to charged pion yields ratio; p_{T}, GeV/c
    ; #frac{K^{+} + K^{-}}{#pi^{+} + #pi^{-}}"
    """
    mc.SetTitle(title)
    mc.label = "PYTHIA8, #sqrt{s} = 13 TeV"
    data.SetTitle(title)
    data.label = "ALCIE, #sqrt{s} = 13 TeV, preliminary"
    mc.SetAxisRange(0.2, 20, "X")
    mc, data = br.rebin_as(mc, data)
    data.SetAxisRange(0.2, 20, "X")
    return Comparator().compare(data, mc, loggs=loggs)


class DoubleRatioFitter(TransformerBase):
    def __init__(self, fitfunc, plot=False):
        super(DoubleRatioFitter, self).__init__(plot)
        self.fitfunc = fitfunc

    def transform(self, double_ratio, loggs):
        double_ratio.SetMarkerSize(0)
        double_ratio.Fit(self.fitfunc, "R")
        self.fitfunc.SetRange(0, 20)
        title = "Chi2/ndf = " + \
            str(self.fitfunc.GetChisquare() / self.fitfunc.GetNDF())
        double_ratio.SetTitle(title)
        double_ratio.label = "pp at #sqrt{s} = 13 TeV"
        double_ratio.SetName("kaon2pion")
        print(br.pars(self.fitfunc))
        return double_ratio


class KaonToPionDoubleRatio(TransformerBase):
    def __init__(self, options, plot=False):
        super(KaonToPionDoubleRatio, self).__init__()
        double_ratio = ReducePipeline(
            ParallelPipeline([
                ("data", KaonToPionRatioData(options.data)),
                ("mc", KaonToPionRatioMC(options.mc)),
            ]),
            rebin_compare
        )

        self.pipeline = Pipeline([
            ("data_mc_ratio", double_ratio),
            ("fit", DoubleRatioFitter(options.fitfunc, plot)),
        ])
