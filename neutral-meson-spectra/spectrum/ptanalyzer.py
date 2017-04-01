#!/usr/bin/python

import ROOT
from sutils import nicely_draw, get_canvas, wait, area_and_error
from invariantmass import InvariantMass
import json
from options import Options

ROOT.TH1.AddDirectory(False)


class PtDependent(object):
    def __init__(self, name, title, label):
        super(PtDependent, self).__init__()
        self.title = title
        self.label = label
        self.name = name + '_' + filter(str.isalnum, self.label)

    def get_hist(self, bins, data, widths = False):
        from array import array
        hist = ROOT.TH1F(self.name, self.title, len(bins) - 1, array('d', bins))
        if not hist.GetSumw2N(): hist.Sumw2()
        hist.GetXaxis().SetTitle('p_{T}, GeV/c')

        widths = [j - i if widths else 1 for i, j in zip(bins[:-1], bins[1:])]
        [hist.SetBinContent(i + 1, m[0] / w) for i, (m, w) in enumerate(zip(data, widths))]
        [hist.SetBinError(i + 1, m[1] / w) for i, (m, w) in enumerate(zip(data, widths))]
        hist.label = self.label
        return hist 



class PtAnalyzer(object):
        
    def __init__(self, hists, label ='N_{cell} > 3', mode = 'v', options = Options()):
        super(PtAnalyzer, self).__init__()
        # These hists are needed for dynamic binning
        self.hists = hists
        self.label = label
        self.show_img = {'quiet': False, 'q': False , 'silent': False, 's': False, 'dead': False}.get(mode, True)
        self.dead_mode = ('dead' in mode)

        # Configure analysis
        with open(options.ptconfig) as f:
            conf = json.load(f)

        props           = conf[options.particle]
        self.bins       = props['ptedges']
        self.need_rebin = props['need_rebin']
        self.multcanvas = props['multcanvas']
        self.partlabel  = props['partlabel']

        ptbins, rebins = self.divide_into_bins()
        pt_intervals = zip(ptbins[:-1], ptbins[1:])

        assert len(pt_intervals) == len(rebins), 'Number of intervals is not equal to the number of rebin parameters'

        f = lambda x, y: InvariantMass(hists, x, y, options)
        self.masses = map(f, pt_intervals, rebins)


    def divide_into_bins(self):
        """
            This method is needed because then we can redefine it
            for dynamical binning instead of static one.
        """
        return self.bins, self.need_rebin

    def histograms(self, data):
        # Book histograms
        histgenerators = [PtDependent('mass', '%s mass position;;m, GeV/c^{2}' % self.partlabel, self.label),
                          PtDependent('width', '%s peak width ;;#sigma, GeV/c^{2}' % self.partlabel, self.label),
                          PtDependent('spectrum', 'Raw %s spectrum ;;#frac{1}{2 #pi #Delta p_{T} } #frac{dN_{rec} }{dp_{T}}' % self.partlabel, self.label),  
                          PtDependent('chi2ndf', '#chi^{2} / N_{dof} (p_{T});;#chi^{2} / N_{dof}', self.label),
                          PtDependent('npi0', 'Number of %ss in each p_{T} bin;; #frac{dN}{dp_{T}}' % self.partlabel, self.label),  
                          PtDependent('cball_alpha', 'Crystal ball parameter #alpha;; #alpha', self.label),
                          PtDependent('cball_n', 'Crystal ball parameter n;; n', self.label)
                          ]

        # Extract bins
        ptedges, dummy = self.divide_into_bins()

        # Extract the data
        return [histgenerators[i].get_hist(ptedges, d) for i, d in enumerate(zip(*data))]

        
    def number_of_mesons(self, mass, intgr_ranges):
        a, b = intgr_ranges if intgr_ranges else mass.peak_function.fit_range
        area, areae = area_and_error(mass.signal, a, b)
        return area, areae


    def properties(self, mass, intgr_ranges):
        fitfun, background = mass.extract_data() 
        if not (fitfun and background): return [[0, 0]] * 7
        # calculate pi0 values
        area, mmass, sigma = [(fitfun.GetParameter(i), fitfun.GetParError(i)) for i in range(3)]
        npi0 = self.number_of_mesons(mass, intgr_ranges)
        nraw = map(lambda x: x / (mass.pt_range[1] - mass.pt_range[0]) / (2. * ROOT.TMath.Pi()), npi0)

        ndf = fitfun.GetNDF() if fitfun.GetNDF() > 0 else 1
        alpha = (fitfun.GetParameter(3), fitfun.GetParError(3))
        n = (fitfun.GetParameter(4), fitfun.GetParError(4))

        return mmass, sigma, nraw, (fitfun.GetChisquare() / ndf, 0), npi0, alpha, n

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
        return histos


    def draw_all_bins(self, f, name = ''):
        # TODO: Try to understand if there is any possibility to 
        # Cnange canvas size without recreating it.
        #
        canvas = get_canvas(1, 1, True)
        canvas.Clear()
        canvas.Divide(*self.multcanvas)
        for i, m in enumerate(self.masses):
            f(m, canvas.cd(i + 1))
        wait(name + self.label, self.show_img, save=True)

    def draw_ratio(self, name = ''):
        f = lambda x, y: x.draw_ratio(y)
        self.draw_all_bins(f, 'multiple-ratio-' + name)

    def draw_mass(self, name = ''):
        f = lambda x, y: x.draw_mass(y)
        self.draw_all_bins(f, 'multiple-mass-' + name)

    def draw_signal(self, name = ''):
        f = lambda x, y: x.draw_signal(y) 
        self.draw_all_bins(f, 'multiple-signal-' + name)

