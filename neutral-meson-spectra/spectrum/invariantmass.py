#!/usr/bin/python

import ROOT
import json
from parametrisation import CrystalBall
from sutils import get_canvas

def remove_zeros(h, zeros, name = '_cleaned'):
    bins = [(i, h.GetBinContent(i), h.GetBinError(i)) for i in range(1, h.GetNbinsX() + 1) if i not in zeros]
    clean = h.Clone(h.GetName() + '_ratio')
    clean.Reset()
    for i, b, e in bins:
        clean.SetBinContent(i, b)
        clean.SetBinError(i, e)
    return clean


def estimate_error(k, hist, nonzeros):
    lower = [i for i in nonzeros if i] + [k]
    left = max(lower)
    
    upper = [i for i in nonzeros if i] + [k]
    right = max(upper)

    # Handle onesided case
    if right == k: 
        right = left

    if left == k:
        left = right

    err = sum(map(hist.GetBinError, [left, right]))

    # TODO: try different scheme
    hist.SetBinError(i, err / 2.)


class InvariantMass(object):
    with open('config/invariant-mass.json') as f:
        conf = json.load(f)
   
    def __init__(self, inhists, pt_range, nrebin, ispi0, relaxedcb, options, tol = 0.00001):
        super(InvariantMass, self).__init__()
        self.pt_range = pt_range 
        self.nrebin   = nrebin
        self.tol      = tol
        self.pt_label = '%.4g < p_{T} < %.4g' % self.pt_range
        self.options = options
        self.peak_function = CrystalBall(ispi0, relaxedcb)

        # Setup parameters
        self.xaxis_range  = [i * j for i, j in zip(self.peak_function.fit_range, self.conf['xaxis_offsets'])]
        self.legend_pos   = self.conf['legend_pos']
        self.pt_label_pos = self.conf['pt_label_pos']

        # Extract the data
        self.mass, self.mixed = map(self.extract_histogram, inhists)
        self.sigf, self.bgrf = None, None

    def remove_zeros(self, h, zeros, name = '_cleaned'):
        # fitf, bckgrnd = self.peak_function.fit(h)
        # TODO: try some more possibilities

        if 'average' in self.options:
            nonzeros = [i for i in range(1, h.GetNbinsX() + 1) if not i in zeros]
            for i in zeros: estimate_error(i, h, nonzeros)
            return h

        # Default method
        return remove_zeros(h, zeros, name)


    def zero_bins(self, hist):
        return [i for i in range(1, hist.GetNbinsX() + 1) if hist.GetBinContent(i) < self.tol]


    def in_range(self, x):
        a, b = self.pt_range
        return x > a and x < b


    def extract_histogram(self, hist):
        a, b = map(hist.GetYaxis().FindBin, self.pt_range)
        mass = hist.ProjectionX(hist.GetName() + '_%d_%d' % (a, b), a, b)
        mass.SetTitle(self.pt_label + '#events = %d M; M_{#gamma#gamma}, GeV/c^{2}' % (hist.nevents / 1e6))         
        mass.SetLineColor(37)

        if not mass.GetSumw2N():
            mass.Sumw2()

        if self.nrebin: mass.Rebin(self.nrebin)
        return mass


    def estimate_background(self, mass, mixed):
        if not mass.GetEntries(): return None

        # Divide real/mixed
        ratio = mass.Clone()
        ratio = self.remove_zeros(ratio, self.zero_bins(ratio), '_ratio')

        ratio.Divide(mixed)
        ratio.GetYaxis().SetTitle("Real/ Mixed")
        # ratio = remove_zeros(ratio, self.zero_bins(mass), '_ratio')

        if ratio.GetEntries() == 0: return ratio
        fitf, bckgrnd = self.peak_function.fit(ratio)

        mixed.Multiply(bckgrnd)
        mixed.SetLineColor(46)
        return ratio


    def noisy_peak_parameters(self):
        """
            This methods estimates peak and background parameters using only 
            effective mass distribution and without background substraction.

            It's needed for tag and probe analysis.
        """
        peak_and_bkrnd = self.peak_function.fit(self.mass)
        pars = lambda x: [x.GetParameter(i) for i in range(x.GetNpar())] 
        return map(pars, peak_and_bkrnd)


    def substract_background(self, mass, mixed):
        if not mass.GetEntries():
            return mass

        # Substract 
        signal = mass.Clone()
        signal = self.remove_zeros(signal, self.zero_bins(signal), '_signal')
        mixed  = self.remove_zeros(mixed, self.zero_bins(mixed), '_mixed')
        signal.Add(mass, mixed, 1., -1.)
        signal.SetAxisRange(*self.xaxis_range)
        signal.GetYaxis().SetTitle("Real - Mixed")

        # for i, v in range(1, signal.GetNbinsX() + 1):
            # if signal.GetBinContent(i): continue
            # print i, signal.GetBinContent(i), signal.GetBinError(i), v

        return signal


    def extract_data(self):
        if not (self.sigf and self.bgrf):
            self.ratio = self.estimate_background(self.mass, self.mixed)
            self.signal = self.substract_background(self.mass, self.mixed)
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
        if not self.ratio:
            return

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
