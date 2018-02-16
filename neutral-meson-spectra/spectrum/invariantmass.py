#!/usr/bin/python

import ROOT
import json
from parametrisation import PeakParametrisation
from sutils import gcanvas, ticks, in_range
from broot import BROOT as br

# TODO: Move VisualizeMass to separate object ptplotter


class VisualizeMass(object):
    def __init__(self):
        super(VisualizeMass, self).__init__()


    def draw_text(self, hist, text, color = 46, bias = 0):
        # Estimate coordinate
        mass = self.peak_function.opt.fit_mass
        x = mass * self.opt.pt_label_pos[0]

        bins = (hist.GetMaximumBin(), hist.GetMinimumBin())
        bmax, bmin = map(hist.GetBinContent, bins)
        zero = bmax - bmin 
        # print zero

        y = bmin + zero * (self.opt.pt_label_pos[1] + bias)
        # Draw the lable
        tl = ROOT.TLatex()
        tl.SetTextAlign(12)
        tl.SetTextSize(0.06 * (mass > 0.3) + 0.08 * (mass < 0.3));
        tl.DrawLatex(x, y, '#color[%d]{%s}' %(color , text));


    def draw_ratio(self, pad = 0):
        if not self.ratio:
            return

        canvas = pad if pad else gcanvas()
        ticks(canvas)
        canvas.SetTicky(False)

        self.ratio.SetAxisRange(*self.xaxis_range)
        self.ratio.Draw()
        self.draw_text(self.ratio, self.pt_label + ', GeV/c')
        canvas.Update()
        return self.ratio


    def draw_signal(self, pad = 0):
        
        if not self.signal:
            return

        canvas = pad if pad else gcanvas()

        ticks(canvas)
        canvas.SetTicky(False)  

        self.signal.SetAxisRange(*self.xaxis_range)
        self.signal.Draw()
        self.draw_text(self.signal, self.pt_label + ', GeV/c')

        if self.area_error:
            try:
                n, sigma = self.area_error
                self.draw_text(self.signal, '#sigma/N = {0:0.2f} '.format(sigma / n), 37, 0.18)
            except ZeroDivisionError as e:
                print e

        canvas.Update()
        return self.signal


    def draw_mass(self, pad = 0):
        canvas = pad if pad else gcanvas()
        ticks(canvas)
        canvas.SetTicky(False) 

        self.mass.SetAxisRange(*self.xaxis_range)
        legend = ROOT.TLegend(*self.opt.legend_pos)
        legend.SetBorderSize(0)
        legend.SetFillStyle(0)
        
        self.mass.SetTitle(self.mass.GetTitle() + " " + str(self.mass.Integral()))
        self.mass.Draw()
        legend.AddEntry(self.mass, 'data')

        if self.background:
            self.background.Draw('same')
            legend.AddEntry(self.background, 'background')

        legend.Draw('same')
        self.draw_text(self.mass, self.pt_label + ', GeV/c')
        canvas.Update()
        return self.mass 


    def fitted(self):
        return self.bgrf and self.sigf



class InvariantMass(VisualizeMass):
   
    def __init__(self, inhists, pt_range, nrebin, options):
        super(InvariantMass, self).__init__()
        self.pt_range = pt_range 
        self.nrebin = nrebin
        self.opt = options.invmass
        self.pt_label = '%.4g < p_{T} < %.4g' % self.pt_range

        # Setup the fit function
        self.peak_function = PeakParametrisation.get(options.param)
        self.xaxis_range  = [i * j for i, j in zip(self.peak_function.opt.fit_range, self.opt.xaxis_offsets)]

        # Extract the data
        self.mass, self.background = map(self.extract_histogram, inhists)
        self.sigf, self.bgrf = None, None
        self.area_error = None
        self._integration_region = self.peak_function.opt.fit_range
        self.ratio = None
        self.signal = None

        
    @staticmethod
    def ptedges(masses):
        return sorted(set(
                sum([list(i.pt_range) for i in masses], [])
            )
        ) 


    @property
    def integration_region(self):
        return self._integration_region


    @integration_region.setter
    def integration_region(self, value):
        if not value:
            return
        self._integration_region = value


    def extract_histogram(self, hist):
        if not hist:
            return None

        mass = br.project_range(hist, '_%d_%d', *self.pt_range)
        mass.nevents = hist.nevents
        mass.SetTitle(self.pt_label + '  #events = %d M; M_{#gamma#gamma}, GeV/c^{2}' % (mass.nevents / 1e6))         
        mass.SetLineColor(37)

        if not mass.GetSumw2N():
            mass.Sumw2()

        if self.nrebin: 
            mass.Rebin(self.nrebin)
        return mass


    def number_of_mesons(self):
        area, areae = br.area_and_error(self.signal, *self.integration_region)
        self.area_error = area, areae
        return area, areae
