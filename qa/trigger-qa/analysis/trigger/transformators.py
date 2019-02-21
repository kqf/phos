import numpy as np
from trigger.utils import style


class RatioCalculator(object):
    def __init__(self, in_cols, out_col):
        super(RatioCalculator, self).__init__()
        self.in_cols = in_cols
        self.out_col = out_col

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X[self.out_col] = X[self.in_cols].apply(
            lambda x: self.ratio(*x), axis=1)
        return X

    def ratio(self, numerator, denominator):
        divided = numerator.Clone("{}_{}".format(
            numerator.GetName(),
            self.out_col))
        divided.Divide(numerator, denominator, 1, 1, "B")
        return divided


class FunctionTransformer(object):
    def __init__(self, in_cols, out_col, func):
        super(FunctionTransformer, self).__init__()
        self.in_cols = in_cols
        self.out_col = out_col
        self.func = func

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        if type(self.in_cols) == str:
            X[self.out_col] = X[self.in_cols].apply(self.func)
        else:
            X[self.out_col] = X[self.in_cols].apply(self.func, axis=1)

        return X


class RebinTransformer(object):
    _bins = np.array([0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8,
                      2.0, 2.2, 2.4, 2.6, 2.8, 3.0, 3.2, 3.4, 3.6, 3.8,
                      4.0, 4.2, 4.4, 4.6, 4.8, 5.0, 5.5, 6.0, 6.5, 7.0,
                      7.5, 8.0, 9.0, 10., 12., 14., 20., 30., 40.])

    def __init__(self, in_cols, out_col):
        super(RebinTransformer, self).__init__()
        self.in_cols = in_cols
        self.out_col = out_col

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X[self.out_col] = X[self.in_cols].apply(self.rebin)
        return X

    def rebin(self, hist):
        rebinned = hist.Rebin(len(self._bins) - 1, hist.GetName(), self._bins)
        rebinned.Sumw2()
        for i in range(1, len(self._bins)):
            delta = self._bins[i] - self._bins[i - 1]
            rebinned.SetBinContent(i, rebinned.GetBinContent(i) / delta)
        style(rebinned)
        return rebinned
