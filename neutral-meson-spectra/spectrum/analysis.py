#!/usr/bin/python

from processing import DataSlicer, RangeEstimator, DataExtractor, MassFitter
from output import AnalysisOutput
from options import Options


class Analysis(object):

    def __init__(self, options=Options()):
        super(Analysis, self).__init__()
        self.options = options
        self._outputs = None

    def transform(self, inputs):
        outputs = AnalysisOutput(inputs.label)
        pipeline = [
            inputs,
            # TODO: Clean this part in pipeline
            # TODO: Add parametrization configuration here
            DataSlicer(self.options.pt, self.options), 
            MassFitter(self.options),
            RangeEstimator(self.options.spectrum),
            DataExtractor(self.options.output)
        ]

        data = None
        for estimator in pipeline:
            data = estimator.transform(data, outputs)

        return data