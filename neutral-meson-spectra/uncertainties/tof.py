from spectrum.analysis import Analysis
from spectrum.transformer import TransformerBase
from spectrum.options import Options
from spectrum.pipeline import Pipeline, HistogramSelector
from spectrum.pipeline import FitfunctionAssigner
from spectrum.pipeline import ComparePipeline
from spectrum.pipeline import OutputDecorator


class TofUncertaintyOptions(object):

    def __init__(self):
        super(TofUncertaintyOptions, self).__init__()
        self.data = Options()
        self.isolated = Options()
        # NB: Don"t assingn to get an exception
        self.fitf = None
        self.decorate = self.data.particle, "isolated"


class TofUncertainty(TransformerBase):

    def __init__(self, options, plot=False):
        super(TofUncertainty, self).__init__(plot)
        self.pipeline = ComparePipeline([
            ('25ns', Pipeline([
                ("reconstruction", Analysis(options.data, plot)),
                ("spectrum", HistogramSelector("spectrum", plot)),
                ("FitF", FitfunctionAssigner(options.fitf, plot)),
            ])),
            ('isolated', Pipeline([
                ("ReconstructMesons", Analysis(options.isolated, plot)),
                ("spectrum", HistogramSelector("spectrum", plot)),
                ("decorate", OutputDecorator(*options.decorate)),
            ])),
        ], True)
