from spectrum.options import Options
from spectrum.spectrum import Spectrum
from spectrum.comparator import Comparator
from spectrum.input import NoMixingInput, Input

from spectrum.broot import BROOT as br
from spectrum.transformer import TransformerBase
from spectrum.pipeline import ComparePipeline, Pipeline, HistogramSelector
from spectrum.analysis import Analysis


class FeeddownEstimator(TransformerBase):
    def __init__(self, options, plot=False):
        super(FeeddownEstimator, self).__init__(plot)
        self.pipeline = ComparePipeline([
            ("feeddown",
                Pipeline([
                    ("analysis", Analysis(options.feeddown)),
                    ("npi0", HistogramSelector("npi0"))
                ])
             ),
            ("regular",
                Pipeline([
                    ("analysis", Analysis(options.regular)),
                    ("npi0", HistogramSelector("npi0"))
                ])
             ),
        ], plot)

# class FeeddownEstimator(object):

#     _hname = "MassPt_#pi^{0}_feeddown_"
#     _label = "feeddown"

#     def __init__(self,
#                  infile,
#                  selection,
#                  fit_function,
#                  options=Options()
#                  ):
#         super(FeeddownEstimator, self).__init__()
#         self.infile = infile
#         # NB: Options should be shared globally to fix the parameters
#         self.options = options
#         self.selection = selection
#         self.fit_function = fit_function
#         self.baseline = self._baseline()

#     def _spectrum(self, infile, selection, histname, label):
#         inputs_ = NoMixingInput(
#             infile,
#             selection,
#             histname
#         )
#         estimator = Spectrum(inputs_, self.options)
#         spectrum = estimator.evaluate().spectrum
#         spectrum.label = label if label else "all"
#         return br.scalew(spectrum)

#     def estimate(self, ptype="", stop=True):
#         feeddown = self._spectrum(
#             self.infile,
#             self.selection,
#             self._hname + ptype,
#             ptype
#         )

#         diff = Comparator((1, 1), stop=stop)
#         result = diff.compare(feeddown, self.baseline)
#         result.label = ptype if ptype else "all secondary"

#         return result, br.confidence_intervals(result, self.fit_function)

#     def _baseline(self):
#         inputs = Input(
#             self.infile,
#             self.selection,
#             "MassPt",
#             "\pi^{0}_{rec} all"
#         )

#         base = Spectrum(inputs, self.options).evaluate().spectrum
#         base.priority = -1
#         br.scalew(base)
#         self.options.spectrum.fit_mass_width = False
#         return base
