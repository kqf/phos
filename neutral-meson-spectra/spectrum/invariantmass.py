#!/usr/bin/python

import ROOT
from parametrisation import CrystalBall
from sutils import get_canvas

class InvariantMass(object):
    def __init__(self, rawhist, mixhist, pt_range, ispi0peak):
        super(InvariantMass, self).__init__()
        self.pt_range = pt_range 
        self.pt_label = '%.4g < P_{T} < %.4g' % self.pt_range
        self.peak_function = CrystalBall(ispi0peak)

        # Extract mass in the pt_bin
        self.mass = self.extract_histogram(rawhist)
        self.mixed = self.extract_histogram(mixhist)
        self.sigf, self.bgrf = None, None



    def extract_histogram(self, hist):
        a, b = map(hist.GetYaxis().FindBin, self.pt_range)
        # suff = 'mixed' if 'mix' in hist.GetName().lower() else 'real'
        mass = hist.ProjectionX(hist.GetName() + '_%d_%d' % (a, b), a, b)
        mass.SetTitle(self.pt_label + '#events = %d M; M_{#gamma#gamma}, GeV/c^{2}' % (hist.nevents / 1e6))         
        mass.SetLineColor(37)
        # mass.Rebin(5)
        # mass.Scale(1./ 5)
        return mass


    def estimate_background(self):
        if self.mass.GetEntries() == 0: return
        zero_bins = [i for i in range(1, self.mass.GetNbinsX()) if self.mass.GetBinContent(i) < 0.00001]

        # Divide real/mixed
        self.ratio = self.mass.Clone()
        self.ratio.Divide(self.mixed)
        self.ratio.GetYaxis().SetTitle("Real/ Mixed")
        [self.ratio.SetBinContent(i, 0) for i in zero_bins]
        
        if self.ratio.GetEntries() == 0: return
        fitf, bckgrnd = self.peak_function.fit(self.ratio)

        self.mixed.Multiply(bckgrnd)
        self.mixed.SetLineColor(46)


    def substract_background(self):
        if self.mass.GetEntries() == 0: return self.mass
        # Identify 0 bins. To get throw them out later
        zero_bins = [i for i in range(1, self.mass.GetNbinsX()) if self.mass.GetBinContent(i) < 1]

        # Substract 
        signal = self.mass.Clone()
        signal.Add(self.mass, self.mixed, 1., -1.)
        signal.SetAxisRange(1.5 * self.peak_function.fit_range[0], 0.85 * self.peak_function.fit_range[1])
        signal.GetYaxis().SetTitle("Real - Mixed")

        # Reset zero bins
        [signal.SetBinContent(i, 0) for i in zero_bins]
        return signal


    def extract_data(self):
        if not (self.sigf and self.bgrf):
            self.estimate_background()
            self.signal = self.substract_background()
            self.sigf, self.bgrf = self.peak_function.fit(self.signal)
        return self.sigf, self.bgrf


    def draw_ratio(self, pad = 0):
        canvas = pad if pad else get_canvas()
        # canvas.SetTickx()
        canvas.SetTicky()  
        self.ratio.SetAxisRange(1.5 * self.peak_function.fit_range[0], 0.85 * self.peak_function.fit_range[1])
        self.ratio.Draw()
        canvas.Update()


    def draw_mass(self, pad = 0):
        canvas = pad if pad else get_canvas()
        # canvas.SetTickx()
        canvas.SetTicky() 

        self.mass.SetAxisRange(1.5 * self.peak_function.fit_range[0], 0.85 * self.peak_function.fit_range[1])
        legend = ROOT.TLegend(0.6, 0.6, 0.8, 0.8)
        legend.SetBorderSize(0)
        legend.SetFillStyle(0)

        self.mass.Draw()
        self.mixed.Draw('same')

        legend.AddEntry(self.mass, 'data')
        legend.AddEntry(self.mixed, 'background')
        legend.Draw('same')
        canvas.Update()

        
    def draw_signal(self, pad = 0):
        canvas = pad if pad else get_canvas()
        # canvas.SetTickx()
        canvas.SetTicky() 

        self.signal.SetAxisRange(1.5 * self.peak_function.fit_range[0], 0.85 * self.peak_function.fit_range[1])
        self.signal.Draw()
        canvas.Update()
