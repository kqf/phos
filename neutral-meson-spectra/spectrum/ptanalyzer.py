#!/usr/bin/python

import ROOT
import collections

from ptplotter import PtPlotter
from outputcreator import OutputCreator, SpectrumExtractor
from invariantmass import InvariantMass, InvariantMassNoMixing
from options import Options

from broot import BROOT as br

ROOT.TH1.AddDirectory(False)

class PtAnalyzer(object):

    def __init__(self, hists, options = Options()):
        super(PtAnalyzer, self).__init__()
        self.hists = self._hists(hists)
        self.nevents = self.hists[0].nevents
        self.opt = options.pt
        self.OutType = collections.namedtuple('SpectrumAnalysisOutput', self.opt.output_order)
        self.extractor = SpectrumExtractor(self.opt.output_order)

        intervals = zip(self.opt.ptedges[:-1], self.opt.ptedges[1:])
        assert len(intervals) == len(self.opt.rebins), 'Number of intervals is not equal to the number of rebin parameters'

        mass_algorithm = InvariantMass if self.opt.use_mixed else InvariantMassNoMixing
        f = lambda x, y: mass_algorithm(self.hists, x, y, options)
        self.masses = map(f, intervals, self.opt.rebins)
        self.plotter = PtPlotter(self.masses, self.opt)

    @staticmethod
    def _hists(hists):
        try:
            iter(hists)
            return hists
        except TypeError:
            return hists.read()


    def histograms(self, data):
        # Don't use format, as it confuses root/latex syntax
        f = lambda x, y: OutputCreator(x, y % self.opt.partlabel, self.opt.label, self.opt.priority)

        # Create actual output
        output = {name: f(name, title) for name, title in self.opt.output.iteritems()}

        # Extract the data
        output = {quant: output[quant].get_hist(self.opt.ptedges, d) for quant, d in zip(self.opt.output_order, zip(*data))}

        # Convert to a proper 
        result = self.OutType(**output)

        # Scale by the number of events 
        result.spectrum.Scale(1. / self.nevents)
        result.spectrum.logy = True
        result.npi0.logy = True
        return  result

        
    # TODO: Move All Serialization logic to OutputCreator
    def quantities(self, draw = True, intgr_ranges = []):
        values = map(self.extractor.eval, self.masses, intgr_ranges)

        # Create hitograms
        histos = self.histograms(values)
        
        if self.opt.dead_mode: 
            return histos

        self.plotter.draw(intgr_ranges, draw)
        return histos

