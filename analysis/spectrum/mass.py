from __future__ import print_function
import ROOT
import six

import spectrum.sutils as su
import spectrum.broot as br


class MassTransformer(object):
    # Reduce all outputs to a single column
    result_type = "reduce"

    def transform(self, data, loggs):
        data[self.out_cols] = data[self.in_cols].apply(
            lambda data: self.apply(
                *data[self.in_cols]), axis=1, result_type=self.result_type)
        return data


class BackgroundEstimator(MassTransformer):
    in_cols = ["measured_fitter", "measured"]
    out_cols = ["background", "measuredf"]
    result_type = "expand"

    def apply(self, measured_fitter, measured):
        signalf, bgrf = measured_fitter.fit(measured)
        bgrf.SetLineColor(ROOT.kRed + 1)
        bgrf.SetFillColor(ROOT.kRed + 1)
        bgrf.SetFillStyle(3436)
        return bgrf, signalf


class SignalExtractor(MassTransformer):
    in_cols = ["measured", "background", "fit_range"]
    out_cols = "signal"

    def apply(self, measured, background, fit_range):
        # Subtraction
        # imass.measured = measured
        # imass.background = background
        signal = measured.Clone()
        signal.Add(background, -1.)
        signal.SetAxisRange(*fit_range)
        signal.GetYaxis().SetTitle("Real - background")
        return signal


class SignalFitter(MassTransformer):
    in_cols = ["signal_fitter", "signal"]
    out_cols = "signalf"

    def apply(self, signal_fitter, signal):
        signalf, bgrf = signal_fitter.fit(signal)
        signalf.SetLineStyle(9)
        return signalf


class SignalFitExtractor(MassTransformer):
    result_type = "expand"
    types = "", "_error"
    mappings = {
        "mass": "M",
        "width": "#sigma",
        "cball_n": "n",
        "cball_alpha": "#alpha",
    }

    def __init__(self, in_cols=["signalf"], prefix=""):
        self.in_cols = in_cols
        self.order = tuple(self.mappings.keys())
        self.out_cols = [
            "{}{}{}".format(prefix, col, error) for col in self.order
            for error in self.types
        ]

    def apply(self, function):
        output = [self._par(function, self.mappings[o]) for o in self.order]
        return sum(output, [])

    def _par(self, func, parname):
        position = func.GetParNumber(parname)

        if position < 0:
            return [0, 0]

        par = func.GetParameter(position)
        par_error = func.GetParError(position)
        return [par, par_error]


class FitQualityExtractor(MassTransformer):
    result_type = "expand"
    out_cols = ["chi2", "chi2_error"]

    def __init__(self, in_cols=["signalf"], prefix=""):
        self.out_cols = ["{}{}".format(prefix, col) for col in self.out_cols]
        self.in_cols = in_cols

    def apply(self, function):
        return br.chi2ndf(function), 0


class MixingBackgroundEstimator(MassTransformer):
    in_cols = ["measured_fitter", "measured", "background"]
    out_cols = ["signal", "measuredf"]
    result_type = "expand"

    def apply(self, measured_fitter, measured, background):
        ratio = br.ratio(measured, background, '')
        ratio.GetYaxis().SetTitle("Same event / mixed event")

        fitf, bckgrnd = measured_fitter.fit(ratio)
        background.Multiply(bckgrnd)
        background.SetLineColor(46)
        return measured, fitf


class ZeroBinsCleaner(MassTransformer):
    """
    Warning: this estimator mutates masses and backgrounds
    The problem:
        there are empty bins in same-event and in mixed-event distributions
        it's not a well determined operation when subtracting empty - nonempty
        replace empty bins with interpolations
    """
    in_cols = ["measured_fitter", "measured", "background", "fit_range", "tol"]
    out_cols = "measured", "background"

    def apply(self, measured_fitter, measured, background, fit_range, tol):
        zeros = set()
        zsig = br.empty_bins(measured, tol)

        # if measured.background else []
        zmix = br.empty_bins(background, tol)
        zeros.symmetric_difference_update(zsig)
        zeros.symmetric_difference_update(zmix)

        # Remove all zero bins and don't
        # touch bins that are zeros in both cases.
        #
        return (
            self._clean(measured, zeros, measured_fitter,
                        fit_range, tol, False),
            self._clean(background, zeros, measured_fitter,
                        fit_range, tol, True)
        )

    def _clean(self, h, zeros, fitter, fit_range, tol, is_background):
        if not zeros:
            return h

        fitf, bckgrnd = fitter.fit(h, is_mixing=is_background)

        # If we failed to fit: do nothing
        if not (fitf and bckgrnd):
            return

        # Delete bin only if it's empty
        def valid(i):
            return h.GetBinContent(i) < tol and \
                su.in_range(h.GetBinCenter(i), fit_range)

        centers = {i: h.GetBinCenter(i) for i in zeros if valid(i)}
        for i, c in six.iteritems(centers):
            res = fitf.Eval(c)
            if res < 0:
                # msg  = 'Warning zero bin found at '
                # print(msg, measured.pt_label, ', measured: ', c)
                res = 0
            h.SetBinError(i, res ** 0.5)
        return h
