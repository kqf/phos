#!/usr/bin/python

from processing import DataSlicer, RangeEstimator, DataExtractor, MassFitter
from output import AnalysisOutput
from options import Options
from pipeline import Pipeline


class Analysis(object):

    def __init__(self, options=Options()):
        super(Analysis, self).__init__()
        self.options = options
        self._loggs = None

    def transform(self, inputs, loggs):
        pipeline = Pipeline([
            ("input", inputs),
            ("slice", DataSlicer(self.options.pt)),
            ("fitmasses", MassFitter(self.options.invmass)),
            ("ranges", RangeEstimator(self.options.spectrum)),
            ("data", DataExtractor(self.options.output))
        ])

        output = pipeline.transform(None, loggs)
        return output