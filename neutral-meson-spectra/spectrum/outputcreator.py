import ROOT
from broot import BROOT as br
import sutils as su
import collections as coll

class SpectrumExtractor(object):

    def handle_empty_fit(f):
        def wrapper(self, mass):
            if not mass.fitted():
                return (0, 0)
            return f(self, mass)
        return wrapper

    def __init__(self, order = []):
        super(SpectrumExtractor, self).__init__()
        rules = {
            'mass': self.mass,
            'width': self.width,
            'spectrum': self.nraw,
            'chi2': self.chi2,
            'npi0': self.npi0,
            'cball_alpha': self.cball_alpha,
            'cball_n': self.cball_n
        }
        self.quantities = [rules[q] for q in order]

    def parameter(self, mass, parname):
        position = mass.sigf.GetParNumber(parname)
        par = mass.sigf.GetParameter(position)
        par_error = mass.sigf.GetParError(position)
        return par, par_error

    @handle_empty_fit
    def mass(self, mass):
        return self.parameter(mass, "M")

    @handle_empty_fit
    def width(self, mass):
        return self.parameter(mass, "#sigma")

    @handle_empty_fit
    def cball_alpha(self, mass):
        return self.parameter(mass, "#alpha")

    @handle_empty_fit
    def cball_n(self, mass):
        return self.parameter(mass, "n")

    @handle_empty_fit
    def npi0(self, mass):
        return mass.number_of_mesons()

    @handle_empty_fit
    def nraw(self, mass):
        npi0 = mass.number_of_mesons()
        return map(lambda x: x / (2. * ROOT.TMath.Pi()), npi0)

    @handle_empty_fit
    def chi2(self, mass):
        ndf = mass.sigf.GetNDF() 
        ndf = ndf if ndf > 0 else 1
        return (mass.sigf.GetChisquare() / ndf, 0) 

    def eval(self, mass):
        return [f(mass) for f in self.quantities]

    @classmethod
    def extract(klass, order, masses):
        extractor = klass(order)
        return map(extractor.eval, masses)


class OutputCreator(object):
    def __init__(self, name, title, label, priority=999):
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
    def output_histogram(name, title, label, bins, data):
        output = OutputCreator(name, title, label)
        return output.get_hist(bins, data)


    @classmethod
    def output(klass, 
            typename,
            data,
            order,
            ptedges,
            titles, # self.opt.output[quant] % self.opt.partlabel,
            label
        ):

        OutType = coll.namedtuple(typename, order)

        iter_collection = zip(
            order, # Ensure ordering of `data`
            zip(*data)
        )

        # Extract the data
        # Don't use format, as it confuses root/latex syntax
        output = {quant: 
            OutputCreator.output_histogram(
                quant,
                titles[quant],
                label,
                ptedges,
                datapoints
            ) for quant, datapoints in iter_collection
        }

        # Convert to a proper datastructure 
        return OutType(**output)



