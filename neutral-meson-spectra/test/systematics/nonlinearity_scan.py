from spectrum.spectrum import Spectrum
from spectrum.input import Input, read_histogram
from spectrum.sutils import gcanvas, wait
from spectrum.options import Options
from spectrum.comparator import Comparator
from systematic_error import SysError
from spectrum.broot import BROOT as br

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

    def mean(self, nsize):
        hmean = br.clone(self.ratio)
        hmean.Scale(1. / nsize)
        return hmean

    def __add__(self, rhs):
        try:
            self.ratio.Add(rhs.ratio)
        except AttributeError:
            self.ratio = br.clone(rhs.ratio)
            self.ratio.SetTitle('#pi^{0} mass positition / #pi^{0} peak width; p_{T}, GeV/c; m/#sigma')
            self.ratio.label = 'mean'
        return self

    @staticmethod
    def chi2(mean, nonlin):
        mean, sigma = br.bins(mean)
        xi, _ = br.bins(nonlin.ratio)
        result = sum((mean - xi) ** 2 / sigma)
        print result
        return result
        
class Nonlinearity(Chi2Entry):
    def __init__(self, sinput, options):
        super(Nonlinearity, self).__init__()
        spectrum = Spectrum(sinput, options)
        sresults = spectrum.evaluate()
        self.mass, self.width = sresults[0:2]

        # Set Values for different ranges
        self.ranges = extract_range(spectrum.analyzer.hists[0])

        # self.mass, self.width = range(1, 20), range(1, 20)
        self.ratio = br.ratio(self.mass, self.width)
        self.ratio.label = 'a = {0:.2f}, #sigma = {1:.2f}'.format(*self.ranges)

        # Save it to have a reference
        self.spectrum = sresults.spectrum



class NonlinearityScanner(object):

    def __init__(self, stop):
        super(NonlinearityScanner, self).__init__()
        self.infile = 'Pythia-new.root'
        self.sel = 'StudyNonlinOnlyTender'
        self.hname = 'MassPt_%d_%d'
        self.sbins = 11, 11
        self.stop = stop
        self.outsys = SysError(label = 'nonlinearity')

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

        mean_hist = mean.mean(len(nonlinearities))
        diff = Comparator()
        diff.compare([mean_hist] + map(lambda x: x.ratio, nonlinearities[::10]))
        # wait(draw = self.stop or True)

        for nonlin in nonlinearities:
            (xx, yy), val = nonlin.ranges, mean.chi2(mean_hist,  nonlin)
            print chi2_hist.Fill(xx, yy, val)

        chi2_hist.Draw('colz')
        wait(draw = self.stop or True)
        return self.outsys.histogram(nonlinearities[0].spectrum)

