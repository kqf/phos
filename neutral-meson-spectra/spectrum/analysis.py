#!/usr/bin/python

import ROOT
import json
from sutils import gcanvas, wait, adjust_canvas, ticks
from kinematic import KinematicTransformer
from outputcreator import RangeTransformer
from options import Options
from broot import BROOT as br


ROOT.TH1.AddDirectory(False)

class Analysis(object):

    def __init__(self, options = Options()):
        super(Analysis, self).__init__()
        self.options = options
        self.opt = options.spectrum

    def transform(self, data):
        self.label = data.label

        # TODO: add transform method to KinematicTransformer
        analyzer = KinematicTransformer(data, self.options)
        rtransformer = RangeTransformer(self.opt, self.options.pt.ptedges, data.label)
        rtransformer.transform(analyzer.masses)
        return analyzer.quantities(True)