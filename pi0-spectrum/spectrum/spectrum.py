#!/usr/bin/python

import ROOT
import numpy as np
from math import pi
from CrystalBall import ExtractQuantities, Fit
from sutils import draw_and_save, nicely_draw

class PtDependent(object):
    def __init__(self, name, title, label):
        super(PtDependent, self).__init__()
        self.name = name
        self.title = title
        self.label = label

    def get_hist(self, bins, data):
        from array import array
        hist = ROOT.TH1F(self.name, self.title, len(bins) - 1, array('d', bins))
        hist.GetXaxis().SetTitle('P_{T}, GeV/c')
        [hist.SetBinContent(i + 1, m) for i, m in enumerate(data[0])]
        [hist.SetBinError(i + 1, m) for i, m in enumerate(data[1])]
        hist.label = self.label
        return hist 

class PtAnalyzer(object):
    def __init__(self, lst, name= 'hMassPtN3', label ='N_{cell} > 3'):
        super(PtAnalyzer, self).__init__()
        self.nevents = lst.FindObject('TotalEvents').GetEntries()
        self.rawhist = lst.FindObject(name)
        self.rawmix = lst.FindObject('hMix' + name[1:])
        self.label = label
        self.get_fit_range = None

    def divide_into_bins(self, n = 20):
        bins = [0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4, 2.6, 2.8, 3.0, 3.2, 3.4, 3.6, 3.8, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10., 11., 12.,       13., 15., 20.]
        return map(self.rawhist.GetYaxis().FindBin, bins)

    def estimate_background(self, real, mixed):
        canvas = ROOT.gROOT.FindObject('c1')

        ratio = real.Clone()
        ratio.Divide(mixed)
        ratio.GetYaxis().SetTitle("Real/ Mixed")

        fitf, bckgrnd = Fit(ratio)
        canvas.Update()
        canvas.SaveAs('results/ratio' + real.GetName() + '.pdf')

        mixed.Multiply(bckgrnd)

        mixed.SetLineColor(46)

        real.Draw()
        mixed.Draw('same')
        canvas.Update()

        # if self.label != 'Mixing':raw_input()
        real.GetXaxis().SetRangeUser(1.01 * bckgrnd.GetXmin(),  0.99 * bckgrnd.GetXmax());
        return mixed


    def extract_data(self, a, b):
        canvas = ROOT.gROOT.FindObject('c1')
        name = self.rawhist.GetName() + '_%d_%d' % (a, b)
        real, mixed = self.rawhist.ProjectionX(name, a, b), self.rawmix.ProjectionX(name + 'mix', a, b)
        mixed.Sumw2()
        real.Sumw2()


        mixed = self.estimate_background(real, mixed)

        zero_bins = [i for i in range(1, real.GetNbinsX()) if real.GetBinContent(i) < 1]
        if self.label == 'Mixing': 
            real.Add(mixed, -1)
            [real.SetBinContent(i, 0) for i in zero_bins]

            if len(zero_bins) > 410: real.Rebin(2)
            if len(zero_bins) > 600: real.Rebin(2)

            start, stop = 0.05, 0.3
            real.SetAxisRange(1.5 * start, 0.85 * stop)
  

        lower, upper = self.rawhist.GetYaxis().GetBinCenter(a), self.rawhist.GetYaxis().GetBinCenter(b)
        real.SetTitle('%.4g < P_{T} < %.4g #events = %d' % (lower, upper, self.nevents) )
        res = ExtractQuantities(real)# if not self.get_fit_range else ExtractQuantities(real, *self.get_fit_range((upper - lower)/ 2.))
        if self.label == 'Mixing': draw_and_save(real.GetName())
        return res

    def quantities(self):
        ranges = self.divide_into_bins()
        intervals = zip(ranges[:-1], ranges[1:])
        data   = np.array([self.extract_data(a, b) for a, b in intervals]).T

        histgenerators = [PtDependent('mass', '#pi^{0} mass position;;m, GeV/c^{2}', self.label),
                          PtDependent('width', '#pi^{0} peak width ;;#sigma, GeV/c^{2}', self.label),
                          PtDependent('spectrum', 'raw #pi^{0} spectrum ;;#frac{1}{2 #pi #Delta p_{T} } #frac{dN_{rec} }{dp_{T}}', self.label),  
                          PtDependent('chi2ndf', '#chi^{2} / N_{dof} (p_{T});;#chi^{2} / N_{dof}', self.label) ]

        ptedges = map(self.rawhist.GetYaxis().GetBinCenter, ranges)


        m, em, s, es, n, en, chi, echi = data

        n = [n[i] / (b - a) / (2. * pi)     for i, (a, b) in enumerate(intervals)]
        en = [en[i] / (b - a) / (2. * pi)   for i, (a, b) in enumerate(intervals)]

        data = [(m, em), (s, es), (n, en), (chi, echi)]

        histos = [histgenerators[i].get_hist(ptedges, d) for i, d in enumerate(data)] 
        map(nicely_draw, histos)

        # if not self.get_fit_range:
            # self.get_fit_range = self.sigma_dependence(histos[0], histos[1])
            # histos =  self.quantities()
        self.sigma_dependence(histos[0], histos[1])

        return histos

    def sigma_dependence(self, mass, sigma):
        # This is needed to estimate background
        canvas = ROOT.gROOT.FindObject('c1')
        self.fitsigma = ROOT.TF1("fitsigma", "TMath::Exp([0] + [1] * x ) * [2] * x + [3]", 0.999* sigma.GetBinCenter(0), sigma.GetBinCenter(sigma.GetNbinsX()))
        # self.fitsigma = ROOT.TF1("self.fitsigma", "TMath::Sqrt([0] * [0] + [1] * [1] / x * x  + [2] * [2] * x * x)", sigma.GetBinCenter(0), sigma.GetBinCenter(sigma.GetNbinsX()))
        sigma.Draw()
        self.fitsigma.SetParameter(0, 0.11 * 0.11)
        self.fitsigma.SetParameter(1, 0.006)
        self.fitsigma.SetParameter(2, 0)
        self.fitsigma.SetParameter(3, 0)
        sigma.Fit(self.fitsigma, "r")

        # canvas.Clear()
        mass.Draw()
        self.fitmass = ROOT.TF1("fitmass", "[0] + [1] * x  - expo(2)", 0.999* sigma.GetBinCenter(0), sigma.GetBinCenter(sigma.GetNbinsX()))
        self.fitmass.SetParameter(0, 1)
        self.fitmass.SetParameter(1, 1)
        self.fitmass.SetParameter(2, 1)
        mass.Fit(self.fitmass, "r")
        canvas.Update()
        draw_and_save(sigma.GetName())
        return lambda pt: (self.fitmass.Eval(pt) - 3 * self.fitsigma.Eval(pt), self.fitmass.Eval(pt) + 3 * self.fitsigma.Eval(pt))

