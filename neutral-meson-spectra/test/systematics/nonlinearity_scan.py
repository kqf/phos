from spectrum.spectrum import Spectrum
from spectrum.input import Input, read_histogram
from spectrum.sutils import gcanvas, wait
from spectrum.options import Options
from spectrum.comparator import Comparator

import ROOT

import os.path

ROOT.TH1.AddDirectory(False)

def extract_range(hist):
    text = hist.GetTitle()
    return map(float, text.split())

class Chi2Entry(object):

    def __init__(self):
        super(Chi2Entry, self).__init__()

    @classmethod
    def evaluate(klass, nonlins):
        self, nsize = sum(nonlins, klass()), len(nonlins)
        self.mean(nsize)
        return self

    @staticmethod
    def sum_bins(a, b):
        return [r1 + r2 for r1, r2 in zip(a, b)]

    def mean(self, nsize):
        self._mean = [r / nsize for r, invw in zip(self.R, self.width_inv)] 
        self._width = [1. / inv / nsize for inv in self.width_inv]
        # print 'mean', len(self.width_inv)

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
        # print len(self._width)
        sample = zip(rhs.R, self._mean, self._width)
        # for r, m, w in sample:
            # print r, m, w
        res = sum(((r - m) / w) ** 2 for r, m, w in sample)
        # print '>>> ', res
        return res
        
class Nonlinearity(Chi2Entry):
    def __init__(self, sinput, options):
        super(Nonlinearity, self).__init__()
        spectrum = Spectrum(sinput, options)
        sresults = spectrum.evaluate()
        self.mass, self.width = self.extract_values(sresults[0:2])
        # self.mass, self.width = range(1, 20), range(1, 20)
        self.R = [m / w for m, w in zip(self.mass, self.width)]
        self.width_inv = [1. / w for w in self.width]

        # Set Values for different ranges
        self.ranges = extract_range(spectrum.analyzer.hists[0])


    def extract_values(self, histograms):
        f = lambda h : \
         [h.GetBinContent(i + 1) for i in range(h.GetNbinsX())]

        return map(f, histograms)



class NonlinearityScanner(object):

    def __init__(self, stop):
        super(NonlinearityScanner, self).__init__()
        self.infile = 'Pythia-new.root'
        self.sel = 'StudyNonlinOnlyTender'
        self.hname = 'MassPt_%d_%d'
        self.sbins = 2, 2
        self.stop = stop

    def inputs(self):
        x, y = self.sbins
        return (Input(self.infile, self.sel, self.hname % (i, j)).read() for j in range(y) for i in range(x))


    def options(self):
        x, y = self.sbins
        return [Options('x = %d, y = %d' % (i, j), 'd') for j in range(y) for i in range(x)]


    def calculate_ranges(self, nonlins):
        xbins, ybins = self.sbins
        (xmin, ymin), (xmax, ymax) = nonlins[0].ranges, nonlins[-1].ranges
        halfstep = lambda mmin, mmax, nbins: (mmax - mmin) / nbins / 2.

        x_halfstep = halfstep(xmin, xmax, xbins)
        xstart = xmin - x_halfstep
        xstop = xmax + x_halfstep

        y_halfstep = halfstep(ymin, ymax, ybins)
        ystart = ymin - y_halfstep
        ystop = ymax + y_halfstep

        return xbins, xstart, xstop, ybins, ystart, ystop


    def test_systematics(self):
        inputs, options = self.inputs(), self.options()
        nonlinearities = map(Nonlinearity, inputs, options)

        # Total ratio
        mean = Chi2Entry.evaluate(nonlinearities)

        c1 = gcanvas(1, 1, resize = True)
        chi2_hist = ROOT.TH2F('chi2', '#chi^{2} distriubiton; a; #sigma, GeV/c', \
            *self.calculate_ranges(nonlinearities))

        for nonlin in nonlinearities:
            (xx, yy), val = nonlin.ranges, mean.chi2(nonlin)
            # print chi2_hist.Fill(xx, yy, val)

        chi2_hist.Draw('colz')
        wait(draw = self.stop)
        return None

