import unittest

from spectrum.comparator import Comparator
from spectrum.input import Input
from spectrum.options import Options
from spectrum.spectrum import Spectrum


def extract_range(hist):
    text = hist.GetTitle()
    return map(float, text.split())


def halfstep(a, b, n):
    return (b - a) / n


class Nonlinearity(object):
    def __init__(self, sinput, options):
        super(Nonlinearity, self).__init__()
        spectrum = Spectrum(sinput, options)
        sresults = spectrum.evaluate()
        self.mass, self.width = sresults[0:2]

        # Set Values for different ranges
        self.ranges = extract_range(spectrum.analyzer.hists[0])


class NonlinearityAtOptimalParameters(unittest.TestCase):

    def setUp(self):
        self.infile = 'Pythia-new.root'
        self.sel = 'StudyNonlinOnlyTender'
        self.hname = 'MassPt_%d_%d'
        self.sbins = 4, 4
        self.optimal = 3, 1

    def inputs(self, x=None, y=None):
        if not x:
            x, _ = self.sbins
            return (Input(self.infile, self.sel, self.hname % (i, y))
                    for i in range(x))
        if not y:
            _, y = self.sbins
            return (Input(self.infile, self.sel, self.hname % (x, j))
                    for j in range(y))

        x, y = self.sbins
        return (Input(self.infile, self.sel, self.hname % (i, j))
                for j in range(y)
                for i in range(x))

    def options(self, x=None, y=None):
        if not x:
            x, _ = self.sbins
            return (Options('x = %d, y = %d' % (i, y), 'd')
                    for i in range(x))

        if not y:
            _, y = self.sbins
            return (Options('x = %d, y = %d' % (x, j), 'd')
                    for j in range(y))

        x, y = self.sbins
        return (Options('x = %d, y = %d' % (i, j), 'd')
                for j in range(y)
                for i in range(x))

        y_halfstep = halfstep(ymin, ymax, ybins)
        ystart = ymin - y_halfstep
        ystop = ymax + y_halfstep

        return xbins, xstart, xstop, ybins, ystart, ystop

    def compare_parameter(self, pars):
        inps, opts = self.inputs(*pars), self.options(*pars)
        masses = map(lambda x, y: Nonlinearity(x, y).mass, inps, opts)

        diff = Comparator()
        diff.compare(masses)

    def test_compare_a_parameter(self):
        pars = self.optimal[0], None
        self.compare_parameter(pars)

    def test_compare_sigma_parameter(self):
        pars = None, self.optimal[1]
        self.compare_parameter(pars)
