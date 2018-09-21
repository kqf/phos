import ROOT
from broot import BROOT as br
import sutils as su


# TODO: Remove all checks if not: return

class BackgroundEstimator(object):

    def transform(self, mass):
        if not mass.mass.GetEntries():
            return mass.mass

        sigf, bgrf = mass.backgroundp.fit(mass.mass)
        bgrf.SetLineColor(8)
        bgrf.SetFillColor(8)
        bgrf.SetFillStyle(3436)
        mass.background = bgrf
        mass.background_fitted = sigf
        return mass


class SignalExtractor(object):

    def transform(self, mass):
        if not mass.mass or not mass.mass.GetEntries():
            return mass

        if not mass.background:
            mass.signal = mass.mass
            return mass

        # Subtraction
        mass.signal = mass.mass.Clone()
        mass.signal.Add(mass.background, -1.)

        # mass.signal = mass.mass.Clone()
        # mass.signal.Sumw2(True)
        # mass.signal.Add(mass.mass, mass.background.GetHistogram(), 1,  -1.)
        # TODO: SetAxisRange aswell
        mass.signal.SetAxisRange(*mass.xaxis_range)
        mass.signal.GetYaxis().SetTitle("Real - background")
        return mass.signal


class SignalFitter(object):

    def transform(self, mass):
        mass.sigf, mass.bgrf = mass.signalp.fit(mass.signal)
        # mass.mass.Draw()
        # mass.bgrf.Draw("same")
        # canvas = ROOT.gROOT.FindObject("c1")
        # canvas.Update()
        # raw_input("testing the inputs")
        return mass


class MixingBackgroundEstimator(object):

    def transform(self, mass):
        if not mass.mass.GetEntries():
            return mass

        if not mass.background:
            return mass

        ratio = br.ratio(mass.mass, mass.background, '')
        ratio.GetYaxis().SetTitle("Same event / mixed event")

        if ratio.GetEntries() == 0:
            return mass

        fitf, bckgrnd = mass.backgroundp.fit(ratio)
        mass.background.Multiply(bckgrnd)
        mass.background.SetLineColor(46)
        mass.ratio = ratio

        # mass.background = bckgrnd
        mass.background_fitted = fitf
        return mass


class ZeroBinsCleaner(object):
    """
    Warning: this estimator mutates masses and backgrounds
    The problem:
        there are empty bins in same-event and in mixed-event distributions
        it's not a well determined operation when subtracting empty - nonempty
        replace empty bins with interpolations
    """

    def transform(self, mass):
        if not mass.background:
            return mass

        zeros = set()

        zsig = br.empty_bins(mass.mass, mass.opt.tol)

        # if mass.background else []
        zmix = br.empty_bins(mass.background, mass.opt.tol)
        zeros.symmetric_difference_update(zsig)
        zeros.symmetric_difference_update(zmix)

        # Remove all zero bins and don't
        # touch bins that are zeros in both cases.
        #
        mass.mass = self._clean_histogram(mass.mass, zeros, mass)
        mass.background = self._clean_histogram(
            mass.background, zeros, mass, True)
        return mass

    def _clean_histogram(self, h, zeros, mass, is_background=False):
        if 'empty' in mass.opt.average:
            return h

        if not zeros:
            return h

        fitf, bckgrnd = mass.backgroundp.fit(h, is_mixing=is_background)

        # If we failed to fit: do nothing
        if not (fitf and bckgrnd):
            return

        # Delete bin only if it's empty
        def valid(i):
            return h.GetBinContent(i) < mass.opt.tol and \
                su.in_range(h.GetBinCenter(i), mass.xaxis_range)

        centers = {i: h.GetBinCenter(i) for i in zeros if valid(i)}
        for i, c in centers.iteritems():
            res = fitf.Eval(c)
            if res < 0:
                # msg  = 'Warning zero bin found at '
                # print msg, mass.pt_label, ', mass: ', c
                res = 0
            h.SetBinError(i, res ** 0.5)
        return h
