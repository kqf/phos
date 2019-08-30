from __future__ import print_function
import ROOT
import six

import spectrum.sutils as su
from spectrum.broot import BROOT as br


# TODO: Remove all checks if not: return
class MassTransformer(object):
    in_col = "invmasses"

    def transform(self, data, loggs):
        data[self.out_col] = data[self.in_col].apply(self.apply)
        return data


class BackgroundEstimator(MassTransformer):
    in_cols = ["invmasses", "mass"]
    out_col = "background"

    def transform(self, data, loggs):
        data[self.out_col] = data[self.in_cols].apply(self.apply, axis=1)
        return data

    def apply(self, data):
        imass, mass = data[self.in_cols]

        if not mass.GetEntries():
            return mass

        sigf, bgrf = imass._background.fit(mass)
        bgrf.SetLineColor(ROOT.kRed + 1)
        bgrf.SetFillColor(ROOT.kRed + 1)
        bgrf.SetFillStyle(3436)
        imass.background = bgrf
        imass.background_fitted = sigf
        return bgrf


class SignalExtractor(MassTransformer):
    in_cols = ["invmasses", "mass", "background"]
    out_col = "signal"

    def transform(self, data, loggs):
        data[self.out_col] = data[self.in_cols].apply(self.apply, axis=1)
        return data

    def apply(self, data):
        imass, mass, background = data[self.in_cols]
        if not mass or not mass.GetEntries():
            return mass

        # Subtraction
        imass.signal = mass.Clone()
        imass.signal.Add(background, -1.)

        # TODO: SetAxisRange aswell
        imass.signal.SetAxisRange(*imass.mass_range)
        imass.signal.GetYaxis().SetTitle("Real - background")
        return imass.signal


class SignalFitter(MassTransformer):
    in_cols = ["invmasses", "signal"]
    out_col = "signal_fitf"

    def transform(self, data, loggs):
        data[self.out_col] = data[self.in_cols].apply(self.apply, axis=1)
        return data

    def apply(self, data):
        imass, signal = data[self.in_cols]
        imass.sigf, imass.bgrf = imass._signal.fit(signal)
        return imass.sigf


class MixingBackgroundEstimator(MassTransformer):
    in_cols = ["invmasses", "mass", "background"]
    out_col = "signal"

    def transform(self, data, loggs):
        data[self.out_col] = data[self.in_cols].apply(self.apply, axis=1)
        return data

    def apply(self, data):
        imass, mass, background = data[self.in_cols]
        if not mass.GetEntries():
            return mass

        ratio = br.ratio(mass, background, '')
        ratio.GetYaxis().SetTitle("Same event / mixed event")

        if ratio.GetEntries() == 0:
            return mass

        fitf, bckgrnd = imass._background.fit(ratio)
        background.Multiply(bckgrnd)
        background.SetLineColor(46)
        imass.ratio = ratio

        # background = bckgrnd
        imass.background_fitted = fitf
        return mass


class ZeroBinsCleaner(MassTransformer):
    """
    Warning: this estimator mutates masses and backgrounds
    The problem:
        there are empty bins in same-event and in mixed-event distributions
        it's not a well determined operation when subtracting empty - nonempty
        replace empty bins with interpolations
    """
    in_cols = ["invmasses", "mass", "background"]
    out_col = "masses_cleaned"

    def transform(self, data, loggs):
        data[self.in_cols].apply(self.apply, axis=1)
        return data

    def apply(self, data):
        imass, mass, background = data[self.in_cols]
        zeros = set()
        zsig = br.empty_bins(mass, imass.opt.tol)

        # if mass.background else []
        zmix = br.empty_bins(background, imass.opt.tol)
        zeros.symmetric_difference_update(zsig)
        zeros.symmetric_difference_update(zmix)

        # Remove all zero bins and don't
        # touch bins that are zeros in both cases.
        #
        mass = self._clean_histogram(mass, zeros, imass)
        background = self._clean_histogram(background, zeros, imass, True)
        return mass

    def _clean_histogram(self, h, zeros, mass, is_background=False):
        if not mass.opt.clean_empty_bins:
            return h

        if not zeros:
            return h

        fitf, bckgrnd = mass._background.fit(h, is_mixing=is_background)

        # If we failed to fit: do nothing
        if not (fitf and bckgrnd):
            return

        # Delete bin only if it's empty
        def valid(i):
            return h.GetBinContent(i) < mass.opt.tol and \
                su.in_range(h.GetBinCenter(i), mass.mass_range)

        centers = {i: h.GetBinCenter(i) for i in zeros if valid(i)}
        for i, c in six.iteritems(centers):
            res = fitf.Eval(c)
            if res < 0:
                # msg  = 'Warning zero bin found at '
                # print(msg, mass.pt_label, ', mass: ', c)
                res = 0
            h.SetBinError(i, res ** 0.5)
        return h
