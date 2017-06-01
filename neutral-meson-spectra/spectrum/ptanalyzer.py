#!/usr/bin/python

import ROOT
from sutils import nicely_draw, get_canvas, wait, area_and_error
from invariantmass import InvariantMass
import json
from options import Options

ROOT.TH1.AddDirectory(False)


class PtDependent(object):
    def __init__(self, name, title, label, priority = 999, nwidth = False):
        super(PtDependent, self).__init__()
        self.title = title
        self.label = label
        self.name = name + '_' + filter(str.isalnum, self.label)
        self.nwidth = nwidth
        self.priority = priority

    def get_hist(self, bins, data):
        from array import array
        hist = ROOT.TH1F(self.name, self.title, len(bins) - 1, array('d', bins))

        if not hist.GetSumw2N(): 
            hist.Sumw2()

        hist.GetXaxis().SetTitle('p_{T}, GeV/c')
        hist.label = self.label
        hist.priority = self.priority

        for i, (d, e) in enumerate(data):
            hist.SetBinContent(i + 1, d)
            hist.SetBinError(i + 1, e)

        if self.nwidth:
            PtDependent.divide_bin_width(hist)

        return hist 

    @staticmethod
    def divide_bin_width(hist):
        nbins = hist.GetNbinsX()
        for i in range(1, nbins + 1): 
            c, e, w = hist.GetBinContent(i), hist.GetBinError(i), hist.GetBinWidth(i)
            hist.SetBinContent(i, c / w)
            hist.SetBinError(i, e / w)




class PtAnalyzer(object):
        
    def __init__(self, hists, label ='N_{cell} > 3', mode = 'v', options = Options()):
        super(PtAnalyzer, self).__init__()
        # These hists are needed for dynamic binning
        self.hists = hists
        self.label = label
        self.show_img = {'quiet': False, 'q': False , 'silent': False, 's': False, 'dead': False}.get(mode, True)
        self.dead_mode = ('dead' in mode)
        self.options = options

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
        histgenerators = [PtDependent('mass', '%s mass position;;m, GeV/c^{2}' % self.partlabel, self.label, self.options.priority),
                          PtDependent('width', '%s peak width ;;#sigma, GeV/c^{2}' % self.partlabel, self.label, self.options.priority),
                          PtDependent('spectrum', 'Raw %s spectrum ;;#frac{1}{2 #pi #Delta p_{T} } #frac{dN_{rec} }{dp_{T}}' % self.partlabel, self.label, self.options.priority),  
                          PtDependent('chi2ndf', '#chi^{2} / N_{dof} (p_{T});;#chi^{2} / N_{dof}', self.label, self.options.priority),
                          PtDependent('npi0', 'Number of %ss in each p_{T} bin;; #frac{dN}{dp_{T}}' % self.partlabel, self.label, self.options.priority),  
                          PtDependent('cball_alpha', 'Crystal ball parameter #alpha;; #alpha', self.label, self.options.priority),
                          PtDependent('cball_n', 'Crystal ball parameter n;; n', self.label, self.options.priority)
                          ]

        # Extract bins
        ptedges, dummy = self.divide_into_bins()

        # Extract the data
        return [histgenerators[i].get_hist(ptedges, d) for i, d in enumerate(zip(*data))]

        
    def number_of_mesons(self, mass, intgr_ranges):
        a, b = intgr_ranges if intgr_ranges else mass.peak_function.fit_range
        area, areae = area_and_error(mass.signal, a, b)

        # TODO: why do we use  sqrt of range in the normalization
        binw = (mass.pt_range[1] - mass.pt_range[0]) ** 0.5 
        area, areae = area * binw, areae * binw 
        return area, areae


    def properties(self, mass, intgr_ranges):
        fitfun, background = mass.extract_data() 
        if not (fitfun and background): return [[0, 0]] * 7
        # calculate pi0 values
        area, mmass, sigma = [(fitfun.GetParameter(i), fitfun.GetParError(i)) for i in range(3)]
        npi0 = self.number_of_mesons(mass, intgr_ranges)
        nraw = map(lambda x: x / (2. * ROOT.TMath.Pi()), npi0)

        ndf = fitfun.GetNDF() if fitfun.GetNDF() > 0 else 1
        alpha = (fitfun.GetParameter(3), fitfun.GetParError(3))
        n = (fitfun.GetParameter(4), fitfun.GetParError(4))

        return mmass, sigma, nraw, (fitfun.GetChisquare() / ndf, 0), npi0, alpha, n
        

    def quantities(self, draw = True, intgr_ranges = None):
        # Prepare Pt ranges and corresponding M_eff integration intervals
        if not intgr_ranges: intgr_ranges = [None] * len(self.masses)
        values = map(lambda x, i: self.properties(x, i), self.masses, intgr_ranges)

        # Create hitograms
        histos = self.histograms(values)
        if self.show_img: map(nicely_draw, histos)

        if self.dead_mode: 
            return histos

        if not draw:
            return histos
            
        self.draw_ratio(intgr_ranges)
        self.draw_mass(intgr_ranges)
        self.draw_signal(intgr_ranges)

        return histos


    def draw_all_bins(self, f, intgr_ranges, name = ''):
        canvas = get_canvas(1, 1, True)
        canvas.Clear()
        canvas.Divide(*self.multcanvas)
        for i, (m, r) in enumerate(zip(self.masses, intgr_ranges)):
            distr = f(m, canvas.cd(i + 1))

            # Draw integration region, when specified
            if not r: continue
            m.line_low = self.draw_line(distr, r[0])
            m.line_up = self.draw_line(distr, r[1])

        wait(name + self.label, self.show_img, save=True)

    def draw_ratio(self, intgr_ranges, name = ''):
        f = lambda x, y: x.draw_ratio(y)
        self.draw_all_bins(f, intgr_ranges,'multiple-ratio-' + name)

    def draw_mass(self, intgr_ranges, name = ''):
        f = lambda x, y: x.draw_mass(y)
        self.draw_all_bins(f, intgr_ranges,'multiple-mass-' + name)

    def draw_signal(self, intgr_ranges, name = ''):
        f = lambda x, y: x.draw_signal(y) 
        self.draw_all_bins(f, intgr_ranges,'multiple-signal-' + name)

    def draw_line(self, distr, position):
        line = ROOT.TLine(position, distr.GetMinimum(), position, distr.GetMaximum())
        line.SetLineColor(1)
        line.SetLineStyle(7)
        line.Draw()
        return line
