from spectrum.analysis import Analysis
from spectrum.pipeline import TransformerBase
from spectrum.pipeline import Pipeline, HistogramSelector
from spectrum.pipeline import FitfunctionAssigner
from spectrum.pipeline import ComparePipeline
from spectrum.pipeline import OutputDecorator
from spectrum.pipeline import HistogramScaler


class DataMCComparator(TransformerBase):

    def __init__(self, options, histname, plot=False):
        super(DataMCComparator, self).__init__(plot)
        self.pipeline = ComparePipeline([
            ('data', Pipeline([
                ("reconstruction", Analysis(options.data, plot)),
                (histname, HistogramSelector(histname, plot)),
                ("FitF", FitfunctionAssigner(options.fitf, plot)),
            ])),
            ('mc', Pipeline([
                ("ReconstructMesons", Analysis(options.mc, plot)),
                (histname, HistogramSelector(histname, plot)),
                ("scale", HistogramScaler(factor=options.factor)),
                ("decorate", OutputDecorator(*options.decorate)),
            ])),
        ], True)


class Nonlinearity(DataMCComparator):

    def __init__(self, options, plot=False):
        super(Nonlinearity, self).__init__(options, "mass", plot)


class Decalibration(DataMCComparator):

    def __init__(self, options, plot=False):
        super(Decalibration, self).__init__(options, "width", plot)


class Shape(DataMCComparator):

    def __init__(self, options, plot=False):
        super(Shape, self).__init__(options, "nmesons", plot)
