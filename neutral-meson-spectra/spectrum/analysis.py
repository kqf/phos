#!/usr/bin/python

from processing import DataSlicer
from kinematic import KinematicTransformer
from outputcreator import RangeTransformer
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
            RangeTransformer(self.options, label),
            KinematicTransformer(self.options, label)
        ]

        data = None
        for estimator in pipeline:
            data = estimator.transform(data)

        return data