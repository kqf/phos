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
    in_cols = ["invmasses", "measured"]
    out_cols = ["background", "measuredf"]
    result_type = "expand"

    def apply(self, imass, measured):
        signalf, bgrf = imass._measured.fit(measured)
        bgrf.SetLineColor(ROOT.kRed + 1)
        bgrf.SetFillColor(ROOT.kRed + 1)
        bgrf.SetFillStyle(3436)
        imass.measuredf = signalf
        return bgrf, imass.measuredf


class SignalExtractor(MassTransformer):
    in_cols = ["invmasses", "measured", "background"]
    out_cols = "signal"

    def apply(self, imass, measured, background):
        # Subtraction
        # imass.measured = measured
        # imass.background = background
        imass.signal = measured.Clone()
        imass.signal.Add(background, -1.)
        imass.signal.SetAxisRange(*imass.fit_range)
        imass.signal.GetYaxis().SetTitle("Real - background")
        return imass.signal


class SignalFitter(MassTransformer):
    in_cols = ["invmasses", "signal"]
    out_cols = "signalf"

    def apply(self, imass, signal):
        imass.signalf, imass.bgrf = imass._signal.fit(signal)
        imass.signalf.SetLineStyle(9)
        # with su.canvas(): # signal.Draw()
        return imass.signalf


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
            return 0, 0

        par = func.GetParameter(position)
        par_error = func.GetParError(position)
        return [par, par_error]


class MixingBackgroundEstimator(MassTransformer):
    in_cols = ["invmasses", "measured", "background"]
    out_cols = ["signal", "measuredf"]
    result_type = "expand"

    def apply(self, imass, measured, background):
        ratio = br.ratio(measured, background, '')
        ratio.GetYaxis().SetTitle("Same event / mixed event")

        fitf, bckgrnd = imass._measured.fit(ratio)
        background.Multiply(bckgrnd)
        background.SetLineColor(46)
        imass.ratio = ratio

        # background = bckgrnd
        imass.measuredf = fitf
        return measured, imass.measuredf


class ZeroBinsCleaner(MassTransformer):
    """
    Warning: this estimator mutates masses and backgrounds
    The problem:
        there are empty bins in same-event and in mixed-event distributions
        it's not a well determined operation when subtracting empty - nonempty
        replace empty bins with interpolations
    """
    in_cols = ["invmasses", "measured", "background"]
    out_cols = "invmasses"

    def apply(self, imass, measured, background):
        zeros = set()
        zsig = br.empty_bins(measured, imass.opt.tol)

        # if measured.background else []
        zmix = br.empty_bins(background, imass.opt.tol)
        zeros.symmetric_difference_update(zsig)
        zeros.symmetric_difference_update(zmix)

        # Remove all zero bins and don't
        # touch bins that are zeros in both cases.
        #
        measured = self._clean_histogram(measured, zeros, imass)
        background = self._clean_histogram(background, zeros, imass, True)
        return imass

    def _clean_histogram(self, h, zeros, measured, is_background=False):
        if not measured.opt.clean_empty_bins:
            return h

        if not zeros:
            return h

        fitf, bckgrnd = measured._measured.fit(h, is_mixing=is_background)

        # If we failed to fit: do nothing
        if not (fitf and bckgrnd):
            return

        # Delete bin only if it's empty
        def valid(i):
            return h.GetBinContent(i) < measured.opt.tol and \
                su.in_range(h.GetBinCenter(i), measured.fit_range)

        centers = {i: h.GetBinCenter(i) for i in zeros if valid(i)}
        for i, c in six.iteritems(centers):
            res = fitf.Eval(c)
            if res < 0:
                # msg  = 'Warning zero bin found at '
                # print(msg, measured.pt_label, ', measured: ', c)
                res = 0
            h.SetBinError(i, res ** 0.5)
        return h
