#!/usr/bin/python

import ROOT
import json
from analysis import Analysis
from sutils import gcanvas, wait, adjust_canvas, ticks
from options import Options
from broot import BROOT as br
from output import AnalysisOutput


ROOT.TH1.AddDirectory(False)

class Spectrum(object):

    def __init__(self, data, options = Options()):
        super(Spectrum, self).__init__()
        self.data = data
        self.model = Analysis(options)

    def evaluate(self, label="", loggs=None):
        local_loggs = AnalysisOutput(self.data.label + label, self.model.options.particle)
        output = self.model.transform(self.data, local_loggs)

        if loggs:
            local_loggs.plot(stop=False)
            loggs.update(local_loggs)

        if label:
            for h in output:
                h.label = label

        return output