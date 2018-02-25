#!/usr/bin/python

from processing import DataSlicer, RangeEstimator, DataExtractor, MassFitter
from output import AnalysisOutput
from options import Options


class Analysis(object):

    def __init__(self, options=Options()):
        super(Analysis, self).__init__()
        self.options = options
        self._loggs = None

    def transform(self, inputs):
        loggs = AnalysisOutput(inputs.label, self.options.particle)
        pipeline = [
            inputs,
            # TODO: Clean this part in pipeline
            # TODO: Add parametrization configuration here
            DataSlicer(self.options.pt), 
            MassFitter(self.options.invmass),
            RangeEstimator(self.options.spectrum),
            DataExtractor(self.options.output)
        ]

        data = None
        for estimator in pipeline:
            data = estimator.transform(data, loggs)

        loggs.plot(stop=False)
        return data