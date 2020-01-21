import ROOT
import numpy as np
from spectrum.pipeline import TransformerBase
import spectrum.broot as br

try:
    import root_numpy as rp
except ModuleNotFoundError:
    import spectrum.broot as rp


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
        bins = np.asarray(list(map(rp.hist2array, ratios)))
        max_deviations = np.abs(bins).mean(axis=0)
        max_deviations = np.abs(max_deviations - 1.)

        output = ratios[0].Clone()
        output.Reset()
        for i, m in zip(br.hrange(output), max_deviations):
            output.SetBinContent(i, m)
        return output
