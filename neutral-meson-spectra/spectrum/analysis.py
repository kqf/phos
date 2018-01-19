#!/usr/bin/python

from processing import DataSlicer, RangeEstimator, DataExtractor
from options import Options


class Analysis(object):

    def __init__(self, options = Options()):
        super(Analysis, self).__init__()
        self.options = options

    def transform(self, inputs):
        label = inputs.label

        pipeline = [
            inputs,
            DataSlicer(self.options.pt, self.options),
            RangeEstimator(self.options, label),
            DataExtractor(self.options, label)
        ]

        data = None
        for estimator in pipeline:
            data = estimator.transform(data)

        return data