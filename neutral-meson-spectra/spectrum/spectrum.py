#!/usr/bin/python

import ROOT
import json
from analysis import Analysis
from sutils import gcanvas, wait, adjust_canvas, ticks
from kinematic import KinematicTransformer
from options import Options
from broot import BROOT as br
from output import AnalysisOutput


ROOT.TH1.AddDirectory(False)

class Spectrum(object):

    def __init__(self, data, options = Options()):
        super(Spectrum, self).__init__()
        self.data = data
        self.model = Analysis(options)

    def evaluate(self, loggs=None):
        local_loggs = AnalysisOutput(self.data.label, self.model.options.particle)
        output = self.model.transform(self.data, local_loggs)
        local_loggs.plot(stop=False)

        if loggs:
            loggs.update(local_loggs)

        return output


# TODO: Add Options factory for singleParticleMC
class CompositeSpectrum(Spectrum):

    def __init__(self, data, options = Options()):
        super(CompositeSpectrum, self).__init__(data.keys()[0], options)
        self.spectrums = [
            Spectrum(l,
                Options.spmc(rr,
                    particle=options.particle
                )
            ) for l, rr in data.iteritems()
        ]


    def evaluate(self):
        hists = [s.evaluate() for s in self.spectrums]
        ranges = [s.opt.fit_range for s in self.spectrums]

        if len(hists) == 2:
            spectra = map(lambda x: x.spectrum, hists)
            for spec in spectra:
                bin = spec.FindBin(ranges[0][1])
                area = spec.Integral(bin - 1, bin + 1)
                if area:
                    spec.Scale(1. / area)

        # Transpose
        pairs = zip(*hists)
        truncated = [br.sum_trimm(obs_pt, ranges) for obs_pt in pairs]
        for h in truncated:
            h.label = self.label

        # Use the same container as normal analysis
        #
        # TODO: Fix me
        results = hists[0]._make(truncated)
        return results

