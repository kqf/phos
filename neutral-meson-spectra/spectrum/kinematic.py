#!/usr/bin/python

import ROOT
import collections

from ptplotter import PtPlotter
from outputcreator import OutputCreator, SpectrumExtractor
from invariantmass import InvariantMass

from broot import BROOT as br

ROOT.TH1.AddDirectory(False)

class KinematicTransformer(object):

    def __init__(self, options, label):
        super(KinematicTransformer, self).__init__()
        self.opt = options.output
        self.label = label
        self.OutType = collections.namedtuple('SpectrumAnalysisOutput', self.opt.output_order)


    def histograms(self, data, ptedges):
        iter_collection = zip(
            self.opt.output_order, # Ensure ordering of `data`
            zip(*data)
        )

        # Extract the data
        # Don't use format, as it confuses root/latex syntax
        output = {quant: 
            OutputCreator.output_histogram(
                quant,
                self.opt.output[quant] % self.opt.partlabel,
                self.label,
                self.opt.priority,
                ptedges,
                d
            ) for quant, d in iter_collection
        }

        # Convert to a proper datastructure 
        return self.OutType(**output)


    def _decorate_hists(self, histograms, nevents):
        # Scale by the number of events 
        histograms.spectrum.Scale(1. / nevents)
        histograms.spectrum.logy = True
        histograms.npi0.logy = True
        return histograms 

        
    def transform(self, masses):
        extractor = SpectrumExtractor(self.opt.output_order)
        values = map(extractor.eval, masses)

        edges = InvariantMass.ptedges(masses)

        # Create hitograms
        histos = self.histograms(values, edges)

        # Decorate the histograms
        nevents = next(iter(masses)).mass.nevents
        decorated = self._decorate_hists(histos, nevents)

        if self.opt.dead_mode: 
            return decorated 

        self.plotter = PtPlotter(masses, self.opt, self.label)
        self.plotter.draw()
        return decorated 

