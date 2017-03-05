#!/usr/bin/python

import ROOT
from sutils import nicely_draw, get_canvas, wait
from invariantmass import InvariantMass

ROOT.TH1.AddDirectory(False)


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
		
    def __init__(self, lst, label ='N_{cell} > 3', mode = 'v', particle = 'pi0', relaxedcb = False):
        super(PtAnalyzer, self).__init__()

        # self.name = name + '_' + filter(str.isalnum, self.label)
        self.nevents, self.rawhist, self.rawmix = lst
        if not self.rawhist.GetSumw2N(): self.rawhist.Sumw2()
        if not self.rawmix.GetSumw2N(): self.rawmix.Sumw2()

        self.label = label
        self.show_img = {'quiet': False, 'q': False , 'silent': False, 's': False, 'dead': False}.get(mode, True)
        self.dead_mode = ('dead' in mode)
        self.ispi0 = 'pi0' in particle

        ptbins = self.divide_into_bins()
        pt_intervals = zip(ptbins[:-1], ptbins[1:])

        f = lambda x: InvariantMass(self.rawhist, self.rawmix, x, self.ispi0, relaxedcb)
        self.masses = map(f, pt_intervals)


    def divide_into_bins(self):
        bins = [0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4, 2.6, 2.8, 3.0, 3.2, 3.4, 3.6, 3.8, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10., 11., 12., 13., 15., 20.]
        # if not self.ispi0: bins = [1.0, 40]
        if not self.ispi0: bins = [1.0, 2.0, 3., 4., 6, 8, 10, 15, 20]
        return bins

    def histograms(self, data):
        # Book histograms
        histgenerators = [PtDependent('mass', '#pi^{0} mass position;;m, GeV/c^{2}', self.label),
                          PtDependent('width', '#pi^{0} peak width ;;#sigma, GeV/c^{2}', self.label),
                          PtDependent('spectrum', 'raw #pi^{0} spectrum ;;#frac{1}{2 #pi #Delta p_{T} } #frac{dN_{rec} }{dp_{T}}', self.label),  
                          PtDependent('chi2ndf', '#chi^{2} / N_{dof} (p_{T});;#chi^{2} / N_{dof}', self.label),
                          PtDependent('cball_alpha', 'crystall ball parameter   #alpha;; #alpha', self.label),
                          PtDependent('cball_n', 'crystall ball parameter n;; n', self.label)
                          ]

        # Extract bins
        ptedges = self.divide_into_bins()

        # Extract the data
        return [histgenerators[i].get_hist(ptedges, d) for i, d in enumerate(zip(*data))]

    def number_of_mesons(self, mass, intgr_ranges):
        fitfun, background = mass.extract_data() 
        a, b = intgr_ranges if intgr_ranges else mass.peak_function.fit_range
        if self.label == 'testsignal':
            return fitfun.Integral(a, b), fitfun.IntegralError(a, b)

        area, areae = ROOT.Double(), ROOT.Double()
        bin = lambda x: mass.signal.FindBin(x)
        area = mass.signal.IntegralAndError(bin(a), bin(b), areae)

        if self.label == 'naive':
            area = sum(mass.signal.GetBinContent(i) for i in range(1, mass.signal.GetNbinsX() + 1) if mass.signal.GetBinCenter(i) > a and mass.signal.GetBinCenter(i) < b)
            return area, areae

        return area, areae


    def properties(self, mass, intgr_ranges):
        fitfun, background = mass.extract_data() 
        if not (fitfun and background): return [[0, 0]] * 5
        # calculate pi0 values
        area, mmass, sigma = [(fitfun.GetParameter(i), fitfun.GetParError(i)) for i in range(3)]
        nraw = self.number_of_mesons(mass, intgr_ranges)
        nraw = map(lambda x: x / (mass.pt_range[1] - mass.pt_range[0]) / (2. * ROOT.TMath.Pi()), nraw)
        ndf = fitfun.GetNDF() if fitfun.GetNDF() > 0 else 1
        alpha = (fitfun.GetParameter(3), fitfun.GetParError(3))
        n = (fitfun.GetParameter(4), fitfun.GetParError(4))

        return mmass, sigma, nraw, (fitfun.GetChisquare() / ndf, 0), alpha, n

    def quantities(self, intgr_ranges = None):
        # Prepare Pt ranges and corresponding M_eff integration intervals
        if not intgr_ranges: intgr_ranges = [None] * len(self.masses)
        values = map(lambda x, i: self.properties(x, i), self.masses, intgr_ranges)

        # Create hitograms
        histos = self.histograms(values)
        if self.show_img: map(nicely_draw, histos)

        if not self.dead_mode:
            self.draw_ratio()
            self.draw_mass()
            self.draw_signal()

        # print [[h.GetBinContent(i) for i in range(1, h.GetNbinsX())] for h in histos] 
        return histos

    def draw_all_bins(self, m = 6, n = 6, f = lambda x, y: x.draw_ratio(y), name = ''):
        canvas = get_canvas(1, 1, True)
        canvas.Clear()
        canvas.Divide(m, n, 0, 0.01)
        for i, m in enumerate(self.masses):
            f(m, canvas.cd(i + 1))
        wait(name + self.label, self.show_img)

    def draw_ratio(self, name = ''):
        m, n = (6, 6) if self.ispi0 else (3, 3)
        self.draw_all_bins(m, n, lambda x, y: x.draw_ratio(y), 'multiple-ratio-')

    def draw_mass(self, name = ''):
        m, n = (6, 6) if self.ispi0 else (3, 3)
        self.draw_all_bins(m, n, lambda x, y: x.draw_mass(y), 'multiple-mass-')

    def draw_signal(self, name = ''):
        m, n = (6, 6) if self.ispi0 else (3, 3)
        self.draw_all_bins(m, n, lambda x, y: x.draw_signal(y), 'multiple-signal-')

