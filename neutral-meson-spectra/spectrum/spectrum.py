#!/usr/bin/python

from analysis import Analysis
from options import Options
from output import AnalysisOutput


class Spectrum(object):

    def __init__(self, data, options=Options()):
        super(Spectrum, self).__init__()
        self.data = data
        self.model = Analysis(options)

    def evaluate(self, label="", loggs=None):
        local_loggs = AnalysisOutput(
            self.data.label + label, self.model.options.particle)
        output = self.model.transform(self.data, local_loggs)

        if loggs:
            local_loggs.plot(stop=False)
            loggs.update(local_loggs)

        if label:
            for h in output:
                h.label = label

        return output
