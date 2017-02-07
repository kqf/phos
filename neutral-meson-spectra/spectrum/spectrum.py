#!/usr/bin/python

import ROOT
from sutils import draw_and_save, nicely_draw, get_canvas, wait
from InvariantMass import InvariantMass

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
        [hist.SetBinContent(i + 1, m[0]) for i, m in enumerate(data)]
        [hist.SetBinError(i + 1, m[1]) for i, m in enumerate(data)]
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
        self.mass_range = (0.05, 0.3)

        ptbins = self.divide_into_bins()
        pt_intervals = zip(ptbins[:-1], ptbins[1:])

        f = lambda x: InvariantMass(self.rawhist, self.rawmix, x)
        self.masses = map(f, pt_intervals)


    def divide_into_bins(self):
        bins = [0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4, 2.6, 2.8, 3.0, 3.2, 3.4, 3.6, 3.8, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10., 11., 12., 13., 15., 20.]
        return bins

    def histograms(self, data):
        # Book histograms
        histgenerators = [PtDependent('mass', '#pi^{0} mass position;;m, GeV/c^{2}', self.label),
                          PtDependent('width', '#pi^{0} peak width ;;#sigma, GeV/c^{2}', self.label),
                          PtDependent('spectrum', 'raw #pi^{0} spectrum ;;#frac{1}{2 #pi #Delta p_{T} } #frac{dN_{rec} }{dp_{T}}', self.label),  
                          PtDependent('chi2ndf', '#chi^{2} / N_{dof} (p_{T});;#chi^{2} / N_{dof}', self.label),
                          PtDependent('signalbkgrnd', ' S_{signal} / S_{bkgrnd} (p_{T});; signal / bkgr', self.label) ]

        # Extract bins
        ptedges = self.divide_into_bins()

        # Extract the data
        return [histgenerators[i].get_hist(ptedges, d) for i, d in enumerate(zip(*data))]

    def properties(self, mass, intgr_ranges):
        fitfun, background = mass.extract_data() 
        if not (fitfun and background): return [[0, 0]] * 5

        # calculate pi0 values
        area, mmass, sigma = [(fitfun.GetParameter(i), fitfun.GetParError(i)) for i in range(3)]

        # TODO: compare this to analytic formula.
        a, b = intgr_ranges
        nraw = fitfun.Integral(a, b), fitfun.IntegralError(a, b)

        sbkg = background.Integral(a, b)
        # esbkg = background.IntegralError(a, b)
        esbkg = abs(sbkg) ** 0.5 

        ndf = fitfun.GetNDF() if fitfun.GetNDF() > 0 else 1
        sb = nraw[0] / sbkg if sbkg != 0 else 0
        esb = sb * ((nraw[1] / nraw[0])**2 + (esbkg/ sbkg)** 2) ** 0.5 if sbkg != 0  and nraw[0] !=0 else 0

        nraw = map(lambda x: x / (mass.pt_range[1] - mass.pt_range[0]) / (2. * ROOT.TMath.Pi()), nraw)
        return mmass, sigma, nraw, (fitfun.GetChisquare() / ndf, 0), (sb, esb)

    def quantities(self, intgr_ranges = None):
        if intgr_ranges == None: intgr_ranges = self.mass_range
        # Prepare Pt ranges and corresponding M_eff integration intervals
        values = map(lambda x: self.properties(x, intgr_ranges), self.masses)

        # Create hitograms
        histos = self.histograms(values)
        if self.show_img: map(nicely_draw, histos)

        # print [[h.GetBinContent(i) for i in range(1, h.GetNbinsX())] for h in histos] 
        return histos

    def draw_all_bins(self, m = 6, n = 6, f = lambda x, y: x.draw_ratio(y), name = ''):
        canvas = get_canvas()
        canvas.Clear()
        canvas.Divide(m, n, 0, 0.01)
        for i, m in enumerate(self.masses):
            f(m, canvas.cd(i + 1))
        wait(name, True, True)

    def draw_ratio(self, m = 6, n = 6, name = ''):
        self.draw_all_bins(m, n, lambda x, y: x.draw_ratio(y), name)

    def draw_mass(self, m = 6, n = 6, name = ''):
        self.draw_all_bins(m, n, lambda x, y: x.draw_mass(y), name)

    def draw_signal(self, m = 6, n = 6, name = ''):
        self.draw_all_bins(m, n, lambda x, y: x.draw_signal(y), name)




class Spectrum(object):
    def __init__(self, lst, label ='N_{cell} > 3', mode = 'v', nsigmas = 3):
        super(Spectrum, self).__init__()
        self.nsigmas = nsigmas
        self.analyzer = PtAnalyzer(lst, label, mode)

    def evaluate(self):
        quantities = self.analyzer.quantities()
        ranges = self.fit_ranges(quantities)
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
