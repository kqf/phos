#!/usr/bin/python

import ROOT
import numpy as np
from math import pi
from CrystalBall import ExtractQuantities, Fit
from sutils import draw_and_save, nicely_draw

class PtDependent(object):
    def __init__(self, name, title, label):
        super(PtDependent, self).__init__()
        self.title = title
        self.label = label
        self.name = name + '_' + filter(str.isalnum, self.label)

    def get_hist(self, bins, data):
        from array import array
        hist = ROOT.TH1F(self.name, self.title, len(bins) - 1, array('d', bins))
        if not hist.GetSumw2N(): hist.Sumw2()
        hist.GetXaxis().SetTitle('P_{T}, GeV/c')
        [hist.SetBinContent(i + 1, m) for i, m in enumerate(data[0])]
        [hist.SetBinError(i + 1, m) for i, m in enumerate(data[1])]
        hist.label = self.label
        return hist 

class PtAnalyzer(object):
    def __init__(self, lst, label ='N_{cell} > 3', mode = 'v'):
        super(PtAnalyzer, self).__init__()

        self.nevents, self.rawhist, self.rawmix = lst
        if not self.rawhist.GetSumw2N(): self.rawhist.Sumw2()
        if not self.rawmix.GetSumw2N(): self.rawmix.Sumw2()

        self.label = label
        self.show_img = {'quiet': False, 'q': False , 'silent': False, 's': False, 'dead': False}.get(mode, True)
        self.default_range = (0.05, 0.3)
        self.save_img = True
        self.deadmode = 'dead' in mode


    def divide_into_bins(self):
        bins = [0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4, 2.6, 2.8, 3.0, 3.2, 3.4, 3.6, 3.8, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10., 11., 12., 13., 15., 20.]
        return map(self.rawhist.GetYaxis().FindBin, bins)

    def estimate_background(self, real, mixed, intgr_range):
        if real.GetEntries() == 0: return mixed

        canvas = ROOT.gROOT.FindObject('c1')

        # Divide real/mixed
        ratio = real.Clone()
        ratio.Divide(mixed)
        ratio.GetYaxis().SetTitle("Real/ Mixed")
        
        # This parameter changes the final values
        # 
        # ratio.SetAxisRange(0.04, 0.6, 'X')

        # Fit the ratio
        # Change here definition if integration range
        if ratio.GetEntries() == 0: return mixed
        fitf, bckgrnd = Fit(ratio)
        if not self.deadmode: 
            draw_and_save([ratio], name = 'ratio_real_to_mixed', draw= self.show_img, save= self.save_img, suffix = self.label)
        # fitf, bckgrnd = Fit(ratio, intgr_range, name = 'ratio_real_to_mixed', show_img = self.show_img)

        # Scale the mixed distribution
        mixed.Multiply(bckgrnd)
        mixed.SetLineColor(46)

        # Draw the results
        if not self.deadmode:
            real.Draw()
            mixed.Draw('same')
            real.GetXaxis().SetRangeUser(1.01 * bckgrnd.GetXmin(),  0.99 * bckgrnd.GetXmax()); 
            draw_and_save([real, mixed], 'real_and_scaled_background', self.show_img, self.save_img, suffix = self.label)

        return mixed

    def substract_background(self, real, mixed):
        if real.GetEntries() == 0: return real, mixed
        # Identify 0 bins. To get throw them out later
        zero_bins = [i for i in range(1, real.GetNbinsX()) if real.GetBinContent(i) < 1]

        # Substract 
        real.Add(mixed, -1)

        # Reset zero bins
        [real.SetBinContent(i, 0) for i in zero_bins]

        # Take into account the statistics
        if len(zero_bins) > 410: real.Rebin(2)
        if len(zero_bins) > 600: real.Rebin(2)

        # Drawing range
        start, stop = 0.05, 0.3
        real.SetAxisRange(1.5 * start, 0.85 * stop)
        return real, mixed

    def extract_data(self, a, b, intgr_range):
        canvas = ROOT.gROOT.FindObject('c1')

        name = self.rawhist.GetName() + '_%d_%d' % (a, b)
        real, mixed = self.rawhist.ProjectionX(name, a, b), self.rawmix.ProjectionX(name + 'mix', a, b)

        lower, upper = self.rawhist.GetYaxis().GetBinCenter(a), self.rawhist.GetYaxis().GetBinCenter(b)
        real.SetTitle('%.4g < P_{T} < %.4g #events = %d; M_{#gamma#gamma}, GeV/c^{2}' % (lower, upper, self.nevents)) 

        mixed = self.estimate_background(real, mixed, intgr_range)
        # if self.label == 'Mixing': 
        real, mixed = self.substract_background(real, mixed)
  
        res = ExtractQuantities(real, intgr_range)

        if not self.deadmode: 
            draw_and_save([real], 'fit_', self.show_img, self.save_img, suffix = self.label)

        return res

    def histograms(self, data, ranges):
        intervals = zip(ranges[:-1], ranges[1:])

        # Book histograms
        histgenerators = [PtDependent('mass', '#pi^{0} mass position;;m, GeV/c^{2}', self.label),
                          PtDependent('width', '#pi^{0} peak width ;;#sigma, GeV/c^{2}', self.label),
                          PtDependent('spectrum', 'raw #pi^{0} spectrum ;;#frac{1}{2 #pi #Delta p_{T} } #frac{dN_{rec} }{dp_{T}}', self.label),  
                          PtDependent('chi2ndf', '#chi^{2} / N_{dof} (p_{T});;#chi^{2} / N_{dof}', self.label),
                          PtDependent('signalbkgrnd', ' S_{signal} / S_{bkgrnd} (p_{T});; signal / bkgr', self.label) ]

        ptedges = map(self.rawhist.GetYaxis().GetBinCenter, ranges)

        # Extract the data
        m, em, s, es, n, en, chi, echi, sign, esign  = data

        # Calculate the yields
        n = [n[i] / (b - a) / (2. * pi)   for i, (a, b) in enumerate(intervals)]
        en = [en[i] / (b - a) / (2. * pi) for i, (a, b) in enumerate(intervals)]

        # Group the data
        data = [(m, em), (s, es), (n, en), (chi, echi), (sign, esign)]

        # Create the histograms
        return [histgenerators[i].get_hist(ptedges, d) for i, d in enumerate(data)]

    def quantities(self, intgr_ranges = None):
        # Prepare Pt ranges and corresponding M_eff integration intervals
        ranges = self.divide_into_bins()
        if not intgr_ranges: 
            intgr_ranges = [self.default_range] * (len(ranges) - 1)

        # Estimate quantities for every Pt bin
        intervals = zip(ranges[:-1], ranges[1:], intgr_ranges)
        data = np.array([self.extract_data(low_pt, up_pt, c) for low_pt, up_pt, c in intervals]).T

        # Create hitograms
        histos = self.histograms(data, ranges)
        if self.show_img: map(nicely_draw, histos)
        return histos


class Spectrum(object):
    def __init__(self, lst, label ='N_{cell} > 3', mode = 'v', nsigmas = 3):
        super(Spectrum, self).__init__()
        self.nsigmas = nsigmas
        self.analyzer = PtAnalyzer(lst, label, mode)
        self.analyzer.save_img = False

    def evaluate(self):
        quantities = self.analyzer.quantities()
        ranges = self.fit_ranges(quantities)
        self.analyzer.save_img = True
        return self.analyzer.quantities(ranges)

    def fit_ranges(self, quantities):
        mass, sigma = quantities[0:2]
        canvas = ROOT.gROOT.FindObject('c1')
        fitsigma = ROOT.TF1("fitsigma", "TMath::Exp([0] + [1] * x ) * [2] * x + [3]", 0.999* sigma.GetBinCenter(0), sigma.GetBinCenter(sigma.GetNbinsX()))
        # fitsigma = ROOT.TF1("fitsigma", "TMath::Sqrt([0] * [0] + [1] * [1] / x * x  + [2] * [2] * x * x)", sigma.GetBinCenter(0), sigma.GetBinCenter(sigma.GetNbinsX()))
        sigma.Draw()
        fitsigma.SetParameter(0, 0.11 * 0.11)
        fitsigma.SetParameter(1, 0.006)
        fitsigma.SetParameter(2, 0)
        fitsigma.SetParameter(3, 0)
        sigma.Fit(fitsigma, "qr")
        draw_and_save([sigma], draw=True, suffix= self.analyzer.label)

        # canvas.Clear()

        mass.Draw()
        fitmass = ROOT.TF1("fitmass", "TMath::Exp([0] + [1] * x ) * [2] * x + [3]", 0.999* mass.GetBinCenter(0), mass.GetBinCenter(mass.GetNbinsX()))
        # fitmass = ROOT.TF1("fitmass", "TMath::Sqrt([0] * [0] + [1] * [1] / x * x  + [2] * [2] * x * x)", sigma.GetBinCenter(0), sigma.GetBinCenter(sigma.GetNbinsX()))
        # ofile = ROOT.TFile('fitmass.root', 'recreate')
        # mass.Write()
        # ofile.Close()
        fitmass.SetParameter(0, 0.11 * 0.11)
        fitmass.SetParameter(1, 0.006)
        fitmass.SetParameter(2, 0)
        fitmass.SetParameter(3, 0)
        mass.Fit(fitmass, "qr")

        # fitmass = ROOT.TF1("fitmass", "[0] + [1] * x  - expo(2)", 0.999* mass.GetBinCenter(0), mass.GetBinCenter(mass.GetNbinsX()))
        # fitmass.SetParameter(0, 10.99)
        # fitmass.SetParameter(1, 0.037)
        # fitmass.SetParameter(2, 2.38)
        # fitmass.SetParameter(3, 0.0033)
        # mass.Fit(fitmass, "qr")
        draw_and_save([mass], draw=True, suffix= self.analyzer.label)
        if canvas: canvas.Update()
        mass_range = lambda pt: (fitmass.Eval(pt) - self.nsigmas * fitsigma.Eval(pt),
                                 fitmass.Eval(pt) + self.nsigmas * fitsigma.Eval(pt)) 

        pt_values = [mass.GetBinCenter(i + 1) for i in range(mass.GetNbinsX())]
        return map(mass_range, pt_values) 
