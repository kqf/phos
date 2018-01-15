#!/usr/bin/python

import ROOT
import json
from sutils import gcanvas, wait, adjust_canvas, ticks
from kinematic import KinematicTransformer, DataSlicer
from outputcreator import RangeTransformer
from options import Options
from broot import BROOT as br


ROOT.TH1.AddDirectory(False)

class Analysis(object):

    def __init__(self, options = Options()):
        super(Analysis, self).__init__()
        self.options = options
        self.opt = options.spectrum

    def transform(self, inputs):
        label = inputs.label

        pipeline = [
            DataSlicer(self.options),
            RangeTransformer(
                self.opt,
                self.options.pt.ptedges,
                label
            ),
            KinematicTransformer(self.options, label)
        ]

        data = inputs
        for estimator in pipeline:
            data = estimator.transform(data)
        return data