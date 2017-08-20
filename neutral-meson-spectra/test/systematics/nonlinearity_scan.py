from spectrum.spectrum import Spectrum
from spectrum.input import Input, TimecutInput, read_histogram
from spectrum.sutils import get_canvas, adjust_canvas, wait
from spectrum.options import Options
from spectrum.comparator import Visualizer, Comparator
from spectrum.sutils import save_tobject, scalew

import ROOT

import os.path
import unittest



class Chi2Entry(object):

    def __init__(self):
        super(Chi2Entry, self).__init__()

    @staticmethod
    def sum_bins(a, b):
        return (r1 + r2 for r1, r2 in zip(a, b))

    def mean(self):
        self._mean = [r / invw for r, invw in zip(self.R, self.width_inv)] 
        return self._mean

    def __add__(self, rhs):
        try:
            self.R = self.sum_bins(self.R, rhs.R)
            self.width_inv = self.sum_bins(self.width_inv, rhs.width_inv)
        except AttributeError:
            self.R = list(rhs.R)
            self.width_inv = list(rhs.width_inv)
        return self

    def chi2(self, rhs):
        return sum(((r - m)/w) ** 2 for r, m, w in zip(rhs.R, self._mean, rhs.width))
        
class Nonlinearity(Chi2Entry):
    def __init__(self, sinput, options):
        super(Nonlinearity, self).__init__()
        # self.spectrum = Spectrum(sinput, options).evaluate()
        # self.mass, self.width = self.spectrum[0:2]
        self.mass, self.width = range(1, 20), range(1, 20)

        self.R = [m / w for m, w in zip(self.mass, self.width)]
        self.width_inv = [1. / w for w in self.width]

    def extract_masses(self, histograms):
        f = [h.GetBinContent(i + 1) for i in range(h.GetNbinsX())]
        return map(f, histograms)



class NonlinearityParameters(unittest.TestCase):

    def setUp(self):
        self.infile = 'Pythia-deleteme.root'
        self.hname = 'MassPt_%d_%d'
        self.sbins = 10, 10

    def inputs(self):
        x, y = self.sbins
        return (Input(self.infile, self.hname % (i, j)) for j in range(y) for i in range(x))

    def options(self):
        x, y = self.sbins
        return (Options('x = %d, y = %d' % (i, j), 'd') for j in range(y) for i in range(x))

    def testRatio(self):
        inputs, options = self.inputs(), self.options()
        nonlinearities = map(Nonlinearity, inputs, options)

        # Total ratio
        mean = sum(nonlinearities, Chi2Entry())
        print mean.mean()


        x, y = self.sbins
        c1 = get_canvas()
        chi2_hist = ROOT.TH2F('chi2', '#chi^{2} distriubiton; a; #sigma, GeV/c', x, 0, x, y, 0, y)
        for i in range(1, x + 1):
            for j in range(1, y + 1):
                chi2_hist.SetBinContent(i, j, mean.chi2(nonlinearities[i + j]))

        chi2_hist.Draw('colz')
        wait()