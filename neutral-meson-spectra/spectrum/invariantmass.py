#!/usr/bin/python

import ROOT
import json
from parametrisation import PeakParametrisation
from sutils import gcanvas, ticks
from broot import BROOT as br

class InvariantMass(object):
   
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
        self.mass, self.mixed = map(self.extract_histogram, inhists)
        self.sigf, self.bgrf = None, None

    def remove_zeros(self, h, zeros):
        if 'empty' in self.opt.average:
            return h

        if not zeros:
            return h

        fitf, bckgrnd = self.peak_function.fit(h)

        # If we failed to fit: do nothing
        if not (fitf and bckgrnd):
            return 

        # Delete bin only if it's empty
        valid = lambda i: h.GetBinContent(i) < self.opt.tol and \
             self.in_range(h.GetBinCenter(i), self.xaxis_range)

        centers = {i: h.GetBinCenter(i) for i in zeros if valid(i)}
        for i, c in centers.iteritems():
            res = fitf.Eval(c)
            if res < 0:
                print 'Warning zero bin found at ', self.pt_label, ', mass: ', c
                res = 0
            h.SetBinError(i, res ** 0.5 )
        return h


    def in_range(self, x, somerange):
        if not somerange:
            somerange = self.pt_range

        a, b = somerange
        return a < x and x < b


    def extract_histogram(self, hist):
        if not hist:
            return None

        mass = br.project_range(hist, '_%d_%d', *self.pt_range)
        mass.SetTitle(self.pt_label + '  #events = %d M; M_{#gamma#gamma}, GeV/c^{2}' % (hist.nevents / 1e6))         
        mass.SetLineColor(37)

        if not mass.GetSumw2N():
            mass.Sumw2()

        if self.nrebin: 
            mass.Rebin(self.nrebin)
            
        return mass


    def estimate_background(self, mass, mixed):
        if not mass.GetEntries():
            return mass

        if not mixed:
            return mass

        # Divide real/mixed
        ratio = br.ratio(mass, mixed, '')
        ratio.GetYaxis().SetTitle("Real/ Mixed")

        if ratio.GetEntries() == 0:
            return ratio
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
        pars, _ = br.pars(peak_and_bkrnd)
        return pars


    def subtract_background(self, mass, mixed):
        if not mass.GetEntries():
            return mass

        if not mixed:
            return mass

        # Subtraction
        signal = mass.Clone()
        zeros = set()

        zsig = br.empty_bins(signal, self.opt.tol)
        zmix = br.empty_bins(mixed, self.opt.tol)

        zeros.symmetric_difference_update(zsig)
        zeros.symmetric_difference_update(zmix)

        # Remove all zero bins and don't 
        # touch bins that are zeros in both cases.
        #
        
        signal = self.remove_zeros(signal, zeros)
        mixed  = self.remove_zeros(mixed, zeros)

        signal.Add(signal, mixed, 1., -1.)
        signal.SetAxisRange(*self.xaxis_range)
        signal.GetYaxis().SetTitle("Real - Mixed")
        return signal


    def extract_data(self):
        if not (self.sigf and self.bgrf):
            self.ratio = self.estimate_background(self.mass, self.mixed)
            self.signal = self.subtract_background(self.mass, self.mixed)
            self.sigf, self.bgrf = self.peak_function.fit(self.signal)
        return self.sigf, self.bgrf


    def draw_pt_bin(self, hist):
        # Estimate coordinate
        mass = self.peak_function.opt.fit_mass
        x = mass * self.opt.pt_label_pos[0]

        bins = (hist.GetMaximumBin(), hist.GetMinimumBin())
        bmax, bmin = map(hist.GetBinContent, bins)
        zero = bmax - bmin 
        # print zero

        y = bmin + zero * self.opt.pt_label_pos[1]
        # Draw the lable
        tl = ROOT.TLatex()
        tl.SetTextAlign(12)
        tl.SetTextSize(0.06 * (mass > 0.3) + 0.08 * (mass < 0.3));
        tl.DrawLatex(x, y, '#color[46]{' + self.pt_label + ', GeV/c}');



    def draw_ratio(self, pad = 0):
        if not self.ratio:
            return

        canvas = pad if pad else gcanvas()
        ticks(canvas)
        canvas.SetTicky(False)

        self.ratio.SetAxisRange(*self.xaxis_range)
        self.ratio.Draw()
        self.draw_pt_bin(self.ratio)
        canvas.Update()
        return self.ratio


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

        if self.mixed:
            self.mixed.Draw('same')
            legend.AddEntry(self.mixed, 'background')

        legend.Draw('same')
        self.draw_pt_bin(self.mass)
        canvas.Update()
        return self.mass

        
    def draw_signal(self, pad = 0):
        canvas = pad if pad else gcanvas()

        ticks(canvas)
        canvas.SetTicky(False)  

        self.signal.SetAxisRange(*self.xaxis_range)
        self.signal.Draw()
        self.draw_pt_bin(self.signal)
        canvas.Update()

        ofile = ROOT.TFile('signals.root', 'update')
        self.signal.Write()
        # ofile.Write()
        ofile.Close()
        return self.signal
