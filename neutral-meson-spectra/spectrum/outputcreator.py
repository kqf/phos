import ROOT
import collections as coll
from array import array
from broot import BROOT as br


class SpectrumExtractor(object):

    def handle_empty_fit(f):
        def wrapper(self, mass):
            if not mass.fitted():  # TODO: This should be removed?
                return (0, 0)
            try:
                return f(self, mass)
            except AttributeError:
                return (0, 0)
        return wrapper

    def __init__(self, order=[]):
        super(SpectrumExtractor, self).__init__()
        rules = {
            'mass': self.mass,
            'width': self.width,
            'spectrum': self.nmesons,
            'chi2': self.chi2,
            'nmesons': self.nmesons,
            'cball_alpha': self.cball_alpha,
            'cball_n': self.cball_n,
            'background_chi2': self.background_chi2,
            'background_cball_alpha': self.background_cball_alpha,
            'background_cball_n': self.background_cball_n

        }

        self.quantities = [rules[q] for q in order]

    def parameter(self, mass, parname, signal=True):
        position = mass.sigf.GetParNumber(parname)
        hist = mass.sigf if signal else mass.background_fitted
        par = hist.GetParameter(position)
        par_error = hist.GetParError(position)
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
    def nmesons(self, mass):
        return mass.number_of_mesons()

    @handle_empty_fit
    def chi2(self, mass):
        ndf = mass.sigf.GetNDF()
        ndf = ndf if ndf > 0 else 1
        return (mass.sigf.GetChisquare() / ndf, 0)

    @handle_empty_fit
    def background_cball_alpha(self, mass):
        return self.parameter(mass, "#alpha", signal=False)

    @handle_empty_fit
    def background_cball_n(self, mass):
        return self.parameter(mass, "n", signal=False)

    @handle_empty_fit
    def background_chi2(self, mass):
        if not mass.background_fitted:
            return (0, 0)

        ndf = mass.background_fitted.GetNDF()
        ndf = ndf if ndf > 0 else 1
        return (mass.background_fitted.GetChisquare() / ndf, 0)

    def eval(self, mass):
        return [f(mass) for f in self.quantities]

    @classmethod
    def extract(klass, order, masses):
        extractor = klass(order)
        return map(extractor.eval, masses)


def output_histogram(ptrange, name, title, label, bins, data, priority=999):
    if label:
        name = "{}_{}".format(name, filter(str.isalnum, label))

    hist = ROOT.TH1F(name, title,
                     len(bins) - 1, array('d', bins))

    if not hist.GetSumw2N():
        hist.Sumw2()

    hist.label = label
    hist.priority = priority

    for i, (d, e) in enumerate(data):
        hist.SetBinContent(i + 1, d)
        hist.SetBinError(i + 1, e)

    xmin, xmax = ptrange
    for i in br.range(hist):
        if xmin < hist.GetBinCenter(i) < xmax:
            continue
        hist.SetBinError(i, 0)
        hist.SetBinContent(i, 0)

    return hist


def analysis_output(typename, data, order, ptrange, ptedges, titles, label):
    AnalysisOutType = coll.namedtuple(typename, order)

    iter_collection = zip(
        order,  # Ensure ordering of `data`
        zip(*data)
    )

    # Extract the data
    # Don't use format, as it confuses root/latex syntax
    output = {
        quant: output_histogram(
            ptrange,
            quant,
            titles[str(quant)],
            label,
            ptedges,
            datapoints
        ) for quant, datapoints in iter_collection
    }

    # Convert to a proper datastructure
    return AnalysisOutType(**output)
