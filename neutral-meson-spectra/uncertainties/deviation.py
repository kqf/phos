import ROOT
from spectrum.transformer import TransformerBase


def max_value(hist, prec):
    max_value = hist.GetMaximum(prec)
    min_value = hist.GetMinimum(-prec)
    return max(abs(max_value), abs(min_value))


class MaxDeviation(TransformerBase):
    def __init__(self, options=None, max_value=3, plot=False):
        super(MaxDeviation, self).__init__(plot)
        self.options = options
        self.max_value = max_value

    def transform(self, ratio, loggs):
        # Maximal deviation from unity
        error = max_value(ratio, self.max_value) - 1
        output = ROOT.TF1("fMaxDeviation", "pol0", 0, 100)
        output.SetParameter(0, error)
        return output


class MaxDeviationVector(MaxDeviation):

    def transform(self, ratios, loggs):
        max_deviation = max(
            max_value(r, self.max_value) for r in ratios
        )
        # Maximal deviation from unity
        error = max_deviation - 1
        output = ROOT.TF1("fMaxDeviation", "pol0", 0, 100)
        output.SetParameter(0, error)
        return output.GetHistogram().Clone()
