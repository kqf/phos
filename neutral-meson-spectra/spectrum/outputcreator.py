import ROOT
from broot import BROOT as br



class SpectrumExtractor(object):

    def handle_empty_fit(f):
        def wrapper(self, mass, intgr_ranges):
            if not mass.fitted():
                return (0, 0)
            return f(self, mass, intgr_ranges)
        return wrapper

    def __init__(self, arg = None):
        super(SpectrumExtractor, self).__init__()
        # TODO: Setup automatic pipeline
        self.quantities = [
            self.mass,
            self.width,
            self.nraw,
            self.chi2,
            self.npi0,
            self.cball_alpha,
            self.cball_n
        ]

    def parameter(self, mass, parname):
        position = mass.sigf.GetParNumber(parname)
        par = mass.sigf.GetParameter(position)
        par_error = mass.sigf.GetParError(position)
        return par, par_error

    def mass(self, mass, intgr_ranges):
        return self.parameter(mass, "M")

    def width(self, mass, intgr_ranges):
        return self.parameter(mass, "#sigma")

    def cball_alpha(self, mass, intgr_ranges):
        return self.parameter(mass, "#alpha")

    def cball_n(self, mass, intgr_ranges):
        return self.parameter(mass, "n")

    def npi0(self, mass, intgr_ranges):
        return mass.number_of_mesons(intgr_ranges)

    def nraw(self, mass, intgr_ranges):
        npi0 = mass.number_of_mesons(intgr_ranges)
        return map(lambda x: x / (2. * ROOT.TMath.Pi()), npi0)

    def chi2(self, mass, intgr_ranges):
        ndf = mass.sigf.GetNDF() 
        ndf = ndf if ndf > 0 else 1
        return (mass.sigf.GetChisquare() / ndf, 0) 

    @handle_empty_fit
    def eval(self, mass, intgr_ranges):
        return [f(mass, intgr_ranges) for f in self.quantities]


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
        mass.extract_data() 
        extractor = SpectrumExtractor()
        return extractor.eval(mass, intgr_ranges)