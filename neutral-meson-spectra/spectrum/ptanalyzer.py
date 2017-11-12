#!/usr/bin/python

import ROOT
import collections

from sutils import gcanvas, wait
from outputcreator import OutputCreator
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

        intervals = zip(self.opt.ptedges[:-1], self.opt.ptedges[1:])
        assert len(intervals) == len(self.opt.rebins), 'Number of intervals is not equal to the number of rebin parameters'

        mass_algorithm = InvariantMass if self.opt.use_mixed else InvariantMassNoMixing
        f = lambda x, y: mass_algorithm(self.hists, x, y, options)
        self.masses = map(f, intervals, self.opt.rebins)

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


    def properties(self, mass, intgr_ranges):
        fitfun, background = mass.extract_data() 
        if not (fitfun and background): return [[0, 0]] * 7
        # calculate pi0 values
        area, mmass, sigma = zip(*br.pars(fitfun, 3))
        npi0 = mass.number_of_mesons(intgr_ranges)
        nraw = map(lambda x: x / (2. * ROOT.TMath.Pi()), npi0)

        ndf = fitfun.GetNDF() if fitfun.GetNDF() > 0 else 1
        alpha = (fitfun.GetParameter(3), fitfun.GetParError(3))
        n = (fitfun.GetParameter(4), fitfun.GetParError(4))

        return mmass, sigma, nraw, (fitfun.GetChisquare() / ndf, 0), npi0, alpha, n
        

    def quantities(self, draw = True, intgr_ranges = None):
        # Prepare Pt ranges and corresponding M_eff integration intervals
        if not intgr_ranges: intgr_ranges = [None] * len(self.masses)
        values = map(lambda x, i: self.properties(x, i), self.masses, intgr_ranges)

        # Create hitograms
        histos = self.histograms(values)
        
        if self.opt.dead_mode: 
            return histos

        if not draw:
            return histos
            
        self.draw_ratio(intgr_ranges)
        self.draw_mass(intgr_ranges)
        self.draw_signal(intgr_ranges)

        return histos


    def draw_last_bins(self, f, intgr_ranges, name = ''):
        canvas = gcanvas(1, 1, True)
        canvas.Clear()
        canvas.Divide(*self.opt.lastcanvas)
        for i, (m, r) in enumerate(zip(self.masses[-4:], intgr_ranges[-4:])):
            distr = f(m, canvas.cd(i + 1))

            # Draw integration region, when specified
            if not r: continue
            m.line_low = self.draw_line(distr, r[0])
            m.line_up = self.draw_line(distr, r[1])

        wait(name + self.opt.label, self.opt.show_img, save=True)



    def draw_all_bins(self, f, intgr_ranges, name = ''):
        canvas = gcanvas(1, 1, True)
        canvas.Clear()
        canvas.Divide(*self.opt.multcanvas)
        for i, (m, r) in enumerate(zip(self.masses, intgr_ranges)):
            distr = f(m, canvas.cd(i + 1))

            # Draw integration region, when specified
            if not r: continue
            m.line_low = self.draw_line(distr, r[0])
            m.line_up = self.draw_line(distr, r[1])

        wait(name + self.opt.label, self.opt.show_img, save=True)

    def draw_ratio(self, intgr_ranges, name = ''):
        f = lambda x, y: x.draw_ratio(y)
        oname = 'multiple-ratio-{0}-{1}'.format(self.opt.particle, name)
        self.draw_all_bins(f, intgr_ranges, oname)

    def draw_mass(self, intgr_ranges, name = ''):
        f = lambda x, y: x.draw_mass(y)
        oname = 'multiple-mass-{0}-{1}'.format(self.opt.particle, name)
        self.draw_all_bins(f, intgr_ranges, oname)

    def draw_signal(self, intgr_ranges, name = ''):
        f = lambda x, y: x.draw_signal(y) 
        oname = 'multiple-signal-{0}-{1}'.format(self.opt.particle, name)
        self.draw_all_bins(f, intgr_ranges, oname)

        oname = 'multiple-signal-high-pt-{0}-{1}'.format(self.opt.particle, name)
        self.draw_last_bins(f, intgr_ranges, oname)

    def draw_line(self, distr, position):
        if not distr:
            return
        line = ROOT.TLine(position, distr.GetMinimum(), position, distr.GetMaximum())
        line.SetLineColor(1)
        line.SetLineStyle(7)
        line.Draw()
        return line
