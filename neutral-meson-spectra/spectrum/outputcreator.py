import ROOT
from broot import BROOT as br

class OutputCreator(object):
    def __init__(self, name, title, label, priority = 999):
        super(OutputCreator, self).__init__()
        self.title = title
        self.label = label
        self.name = name + '_' + filter(str.isalnum, self.label)
        self.priority = priority

    def get_hist(self, bins, data):
        from array import array
        hist = ROOT.TH1F(self.name, self.title, len(bins) - 1, array('d', bins))

        if not hist.GetSumw2N(): 
            hist.Sumw2()

        hist.label = self.label
        hist.priority = self.priority

        for i, (d, e) in enumerate(data):
            hist.SetBinContent(i + 1, d)
            hist.SetBinError(i + 1, e)
        return hist 

    @staticmethod
    def eval(mass, intgr_ranges):
        fitfun, background = mass.extract_data() 
        if not (fitfun and background): return [[0, 0]] * 7
        # calculate pi0 values
        area, mmass, sigma = zip(*br.pars(fitfun, 3))
        npi0 = mass.number_of_mesons(intgr_ranges)
        nraw = map(lambda x: x / (2. * ROOT.TMath.Pi()), npi0)

        ndf = fitfun.GetNDF() if fitfun.GetNDF() > 0 else 1
        alpha = (fitfun.GetParameter(3), fitfun.GetParError(3))
        n = (fitfun.GetParameter(4), fitfun.GetParError(4))

        return mmass, sigma, nraw, (fitfun.GetChisquare() / ndf, 0), npi0, alpha, n