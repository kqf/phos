#!/usr/bin/python

import ROOT
import json
from parametrisation import CrystalBall
from sutils import get_canvas

def remove_zeros(h, zeros, name = '_cleaned'):
    bins = [(i, h.GetBinContent(i), h.GetBinError(i)) for i in range(1, h.GetNbinsX()) if i not in zeros]
    clean = h.Clone(h.GetName() + '_ratio')
    clean.Reset()
    for i, b, e in bins:
        clean.SetBinContent(i, b)
        clean.SetBinError(i, e)
    return clean

class InvariantMass(object):
    with open('config/invariant-mass.json') as f:
        conf = json.load(f)
   
    def __init__(self, rawhist, mixhist, pt_range, ispi0, relaxedcb):
        super(InvariantMass, self).__init__()
        self.pt_range = pt_range 
        self.pt_label = '%.4g < p_{T} < %.4g' % self.pt_range
        self.peak_function = CrystalBall(ispi0, relaxedcb)

        # Setup parameters
        self.zero_threshold = self.conf['zero_threshold']
        self.need_rebin     = self.conf['needs_rebin']
        self.nrebin         = self.conf['nrebin']
        self.xaxis_range    = [i * j for i, j in zip(self.peak_function.fit_range, self.conf['xaxis_offsets'])]
        self.legend_pos     = self.conf['legend_pos']
        self.pt_label_pos   = self.conf['pt_label_pos']

        # Extract the data
        self.mass = self.extract_histogram(rawhist)
        self.mixed = self.extract_histogram(mixhist)
        self.sigf, self.bgrf = None, None


    def zero_bins(self, hist):
        return [i for i in range(1, hist.GetNbinsX()) if hist.GetBinContent(i) < self.zero_threshold]


    def in_range(self, x):
        a, b = self.pt_range
        return x > a and x < b


    def extract_histogram(self, hist):
        a, b = map(hist.GetYaxis().FindBin, self.pt_range)
        mass = hist.ProjectionX(hist.GetName() + '_%d_%d' % (a, b), a, b)
        mass.SetTitle(self.pt_label + '#events = %d M; M_{#gamma#gamma}, GeV/c^{2}' % (hist.nevents / 1e6))         
        mass.SetLineColor(37)
        if any(map(self.in_range, self.need_rebin)):
            mass.Rebin(self.nrebin)
        return mass


    def estimate_background(self):
        if not self.mass.GetEntries(): return

        # Divide real/mixed
        ratio = self.mass.Clone()
        ratio.Divide(self.mixed)
        ratio.GetYaxis().SetTitle("Real/ Mixed")
        self.ratio = remove_zeros(ratio, self.zero_bins(self.mass), '_ratio')

        if self.ratio.GetEntries() == 0: return
        fitf, bckgrnd = self.peak_function.fit(self.ratio)

        self.mixed.Multiply(bckgrnd)
        self.mixed.SetLineColor(46)


    def substract_background(self):
        if not self.mass.GetEntries():
            return self.mass

        # Substract 
        signal = self.mass.Clone()
        signal.Add(self.mass, self.mixed, 1., -1.)
        signal.SetAxisRange(*self.xaxis_range)
        signal.GetYaxis().SetTitle("Real - Mixed")
        signal = remove_zeros(signal, self.zero_bins(self.mass), '_signal')
        return signal


        
    def extract_data(self):
        if not (self.sigf and self.bgrf):
            self.estimate_background()
            self.signal = self.substract_background()
            self.sigf, self.bgrf = self.peak_function.fit(self.signal)
        return self.sigf, self.bgrf

    def draw_pt_bin(self, hist):
        # Estimate coordinate
        y = (hist.GetMaximum() - hist.GetMinimum()) / self.pt_label_pos[0]
        a, b = self.peak_function.fit_range
        x = self.pt_label_pos[1] * (b - a) / 3
        # Draw the lable
        tl = ROOT.TLatex()
        tl.SetTextAlign(12);
        tl.SetTextSize(0.08);
        tl.DrawLatex(x, y, '#color[46]{' + self.pt_label + ', GeV/c}');



    def draw_ratio(self, pad = 0):
        canvas = pad if pad else get_canvas()
        # canvas.SetTickx()
        canvas.SetTicky()  
        self.ratio.SetAxisRange(*self.xaxis_range)
        self.ratio.Draw()
        self.draw_pt_bin(self.ratio)
        canvas.Update()


    def draw_mass(self, pad = 0):
        canvas = pad if pad else get_canvas()
        # canvas.SetTickx()
        canvas.SetTicky() 

        self.mass.SetAxisRange(*self.xaxis_range)
        legend = ROOT.TLegend(*self.legend_pos)
        legend.SetBorderSize(0)
        legend.SetFillStyle(0)

        self.mass.Draw()
        self.mixed.Draw('same')

        legend.AddEntry(self.mass, 'data')
        legend.AddEntry(self.mixed, 'background')
        legend.Draw('same')
        self.draw_pt_bin(self.mass)
        canvas.Update()

        
    def draw_signal(self, pad = 0):
        canvas = pad if pad else get_canvas()
        # canvas.SetTickx()
        canvas.SetTicky() 
        self.signal.SetAxisRange(*self.xaxis_range)
        self.signal.Draw()
        self.draw_pt_bin(self.signal)
        canvas.Update()
