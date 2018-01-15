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

        # TODO: add transform method to KinematicTransformer
        slicer = DataSlicer(self.options)
        masses = slicer.transform(inputs)
        rtransformer = RangeTransformer(self.opt, self.options.pt.ptedges, inputs.label)
        rtransformer.transform(masses)
        analyzer = KinematicTransformer(self.options, label)
        return analyzer.quantities(masses, True)