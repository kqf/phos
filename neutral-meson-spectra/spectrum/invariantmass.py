#!/usr/bin/python

import ROOT
import json
from parametrisation import CrystalBall
from sutils import get_canvas

class InvariantMass(object):
    with open('config/invariant-mass.json') as f:
        conf = json.load(f)
   
    def __init__(self, inhists, pt_range, nrebin, options, tol = 0.00001):
        super(InvariantMass, self).__init__()
        self.pt_range = pt_range 
        self.nrebin   = nrebin
        self.tol      = tol
        self.pt_label = '%.4g < p_{T} < %.4g' % self.pt_range
        self.options = options

        self.peak_function = CrystalBall(options.ispi0, options.relaxedcb)

        # Setup parameters
        self.xaxis_range  = [i * j for i, j in zip(self.peak_function.fit_range, self.conf['xaxis_offsets'])]
        self.legend_pos   = self.conf['legend_pos']
        self.pt_label_pos = self.conf['pt_label_pos']

        # Extract the data
        self.mass, self.mixed = map(self.extract_histogram, inhists)
        self.sigf, self.bgrf = None, None

    def remove_zeros(self, h, zeros):
        if 'empty' in self.options.average:
            return h

        fitf, bckgrnd = self.peak_function.fit(h)

        # If we failed to fit: do nothing
        if not (fitf and bckgrnd):
            return 

        zeros = {i: c for i, c in zeros.iteritems() if self.xaxis_range[0] < c and c < self.xaxis_range[1]}
        for i, c in zeros.iteritems():
            res = fitf.Eval(c)
            if res < 0:
                print 'Warning zero bin found at ', self.pt_label, ' ,mass: ', c
                res = 0
            h.SetBinError(i, res ** 0.5 )
        return h


    def zero_bins(self, hist, exclude = {}):
        bins = {i: hist.GetBinContent(i) for i in range(1, hist.GetNbinsX() + 1)}

        # All bins that are less then certain value
        zeros = {i: hist.GetBinCenter(i) for i, v in bins.iteritems() if v < self.tol}

        # Don't take into account thos bins that are empty in both histograms
        unique_zeros = {i: v for i, v in zeros.iteritems() if not i in exclude}
        return unique_zeros


    def in_range(self, x):
        a, b = self.pt_range
        return a < x and x < b


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
        ratio.Divide(mixed)
        ratio.GetYaxis().SetTitle("Real/ Mixed")

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

        # Substraction
        signal = mass.Clone()

        # Remove zeros, first one should find zeros! 
        # In this procedure we don't touch bins that are zeros in both cases.
        f = lambda x, y: (x, self.zero_bins(x, self.zero_bins(y)))
        signal = self.remove_zeros(*f(signal, mixed))
        mixed  = self.remove_zeros(*f(mixed, signal))

        signal.Add(signal, mixed, 1., -1.)
        signal.SetAxisRange(*self.xaxis_range)
        signal.GetYaxis().SetTitle("Real - Mixed")
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

        ofile = ROOT.TFile('signals.root', 'update')
        self.signal.Write()
        # ofile.Write()
        ofile.Close()
