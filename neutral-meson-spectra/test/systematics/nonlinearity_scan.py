from spectrum.spectrum import Spectrum
from spectrum.input import Input, TimecutInput, read_histogram
from spectrum.sutils import get_canvas, adjust_canvas, wait
from spectrum.options import Options
from spectrum.comparator import Visualizer, Comparator
from spectrum.sutils import save_tobject, scalew

import ROOT

import os.path
import unittest

ROOT.TH1.AddDirectory(False)

def extract_range(hist):
    text = hist.GetTitle()
    return map(float, text.split())

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
        spectrum = Spectrum(sinput, options)
        # sresults = spectrum.evaluate()
        # self.mass, self.width = self.extract_values(sresults[0:2])
        self.mass, self.width = range(1, 20), range(1, 20)
        self.R = [m / w for m, w in zip(self.mass, self.width)]
        self.width_inv = [1. / w for w in self.width]

        # Set Values for different ranges
        self.ranges = extract_range(spectrum.analyzer.hists[0])

        # for h in sresults:
        #     h.IsA().Destructor(h)

    def extract_values(self, histograms):
        f = lambda h : \
         [h.GetBinContent(i + 1) for i in range(h.GetNbinsX())]

        return map(f, histograms)



class NonlinearityParameters(unittest.TestCase):

    def setUp(self):
        self.infile = 'Pythia-new.root'
        self.sel = 'StudyNonlinOnlyTender'
        self.hname = 'MassPt_%d_%d'
        self.sbins = 5, 5

    def inputs(self):
        x, y = self.sbins
        return (Input(self.infile, self.sel, self.hname % (i, j)).read() for j in range(y) for i in range(x))


    def options(self):
        x, y = self.sbins
        return [Options('x = %d, y = %d' % (i, j), 'd') for j in range(y) for i in range(x)]

    def testRatio(self):
        inputs, options = self.inputs(), self.options()
        nonlinearities = map(Nonlinearity, inputs, options)


        # Total ratio
        mean = sum(nonlinearities, Chi2Entry())
        print mean.mean()

        bmin, bmax = nonlinearities[0].ranges, nonlinearities[-1].ranges
        print bmin
        print bmax


        x, y = self.sbins
        c1 = get_canvas(1, 1, resize = True)
        chi2_hist = ROOT.TH2F('chi2', '#chi^{2} distriubiton; a; #sigma, GeV/c', x, bmin[0], bmax[0], y, bmin[1], bmax[1])
        for i in range(x):
            for j in range(y):
                chi2_hist.SetBinContent(i + 1, j + 1, mean.chi2(nonlinearities[x * i + j]))

        chi2_hist.Draw('colz')
        wait()



