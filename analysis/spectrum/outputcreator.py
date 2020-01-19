import ROOT
import collections
import numpy as np
from array import array

import spectrum.broot as br


class SpectrumExtractor(object):

    def handle_empty_fit(f):
        def wrapper(self, mass):
            try:
                return f(self, mass)
            except AttributeError:
                return (1, 0)
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

    def parameter(self, func, parname):
        position = func.GetParNumber(parname)

        if position < 0:
            return 0, 0

        par = func.GetParameter(position)
        par_error = func.GetParError(position)
        return par, par_error

    @handle_empty_fit
    def mass(self, mass):
        return self.parameter(mass.signalf, "M")

    @handle_empty_fit
    def width(self, mass):
        return self.parameter(mass.signalf, "#sigma")

    @handle_empty_fit
    def cball_alpha(self, mass):
        return self.parameter(mass.signalf, "#alpha")

    @handle_empty_fit
    def cball_n(self, mass):
        return self.parameter(mass.signalf, "n")

    @handle_empty_fit
    def nmesons(self, mass):
        return mass.number_of_mesons()

    @handle_empty_fit
    def chi2(self, mass):
        ndf = mass.signalf.GetNDF()
        ndf = ndf if ndf > 0 else 1
        return mass.signalf.GetChisquare() / ndf, 0

    @handle_empty_fit
    def background_cball_alpha(self, mass):
        return self.parameter(mass.measuredf, "#alpha")

    @handle_empty_fit
    def background_cball_n(self, mass):
        return self.parameter(mass.measuredf, "n")

    @handle_empty_fit
    def background_chi2(self, mass):
        ndf = mass.measuredf.GetNDF()
        ndf = ndf if ndf > 0 else 1
        return mass.measuredf.GetChisquare() / ndf, 0

    def eval(self, mass):
        return [f(mass) for f in self.quantities]

    @classmethod
    def extract(klass, order, masses):
        extractor = klass(order)
        return map(extractor.eval, masses)


# TODO: Check the parameters
def analysis_output(typename, data, order, ptrange, ptedges, titles):
    AnalysisOutType = collections.namedtuple(typename, order)

    iter_collection = zip(
        order,  # Ensure ordering of `data`
        zip(*data)
    )

    # Extract the data
    # Don't use format, as it confuses root/latex syntax
    output = {
        quant: br.table2hist(
            ptrange=ptrange,
            name=quant,
            title=titles[str(quant)],
            bins=ptedges,
            data=datapoints
        ) for quant, datapoints in iter_collection
    }

    # Convert to a proper datastructure
    return AnalysisOutType(**output)
