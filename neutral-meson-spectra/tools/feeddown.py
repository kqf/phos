from spectrum.sutils import wait
from spectrum.options import Options
from spectrum.spectrum import Spectrum
from spectrum.comparator import Comparator
from spectrum.input import NoMixingInput, read_histogram, Input

from spectrum.broot import BROOT as br

import ROOT


class FeeddownEstimator(object):

    def __init__(self, infile, selection, fit_function):
        super(FeeddownEstimator, self).__init__()
        self.infile = infile
        self.fit_function = fit_function
        self.selection = selection
        self.hname = 'MassPt_#pi^{0}_feeddown_'
        self.label = 'feeddown'
        self.baseline = self._baseline()

    def _spectrum(self, infile, selection, histname, label):
        inputs_ = NoMixingInput(
            infile, 
            selection, 
            histname
        )

        # TODO: Use well-defined peak parametrization
        options = Options.fixed_peak()

        estimator = Spectrum(inputs_, options)
        spectrum = estimator.evaluate().spectrum
        spectrum.label = label if label else 'all'
        return br.scalew(spectrum) 

    def estimate(self, ptype = '', stop = True):
        feeddown = self._spectrum(
            self.infile,
            self.selection,
            self.hname + ptype,
            ptype
        )

        diff = Comparator((1, 1), stop = stop)
        result = diff.compare(feeddown, self.baseline)
        result.label = ptype if ptype else 'all secondary'

        # TODO: Is this the right way to estimate Feeddown?
        return result, br.confidence_intervals(result, self.fit_function)


    def _baseline(self):
        # generated = read_histogram(self.infile, self.selection, 'hPt_#pi^{0}', 'generated')
        # br.scalew(generated)
        # Estimate this quantity in a following way

        inputs = Input(
            self.infile,
            self.selection,
            'MassPt',
            '\pi^{0}_{rec} all'
        )
        options = Options()
        options.param.background = 'pol3'
        base = Spectrum(inputs, options).evaluate().spectrum
        base.priority = -1
        br.scalew(base)
        return base

