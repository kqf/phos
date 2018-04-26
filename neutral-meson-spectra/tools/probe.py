from spectrum.analysis import Analysis
from spectrum.transformer import TransformerBase
from spectrum.pipeline import ComparePipeline, Pipeline
from spectrum.pipeline import HistogramSelector, HistogramScaler


class TagAndProbe(TransformerBase):
    def __init__(self, options, plot=False):
        super(TagAndProbe, self).__init__(plot)
        self.pipeline = ComparePipeline([
            ("tof cut",
                Pipeline([
                    ("analysis", Analysis(options.analysis, plot)),
                    ("npi0", HistogramSelector("npi0")),
                    ('scale', HistogramScaler())
                ])
             ),
            ("no cut",
                Pipeline([
                    ("analysis", Analysis(options.analysis, plot)),
                    ("npi0", HistogramSelector("npi0")),
                    ('scale', HistogramScaler())
                ])
             ),
        ], plot)
