import ROOT
from spectrum.transformer import TransformerBase


class MaxDeviation(TransformerBase):
    def __init__(self, options=None, max_value=3, plot=False):
        super(MaxDeviation, self).__init__(plot)
        self.options = options
        self.max_value = max_value

    def transform(self, ratio, loggs):
        max_value = ratio.GetMaximum(3)
        min_value = ratio.GetMinimum(-3)
        max_deviation = max(abs(max_value), abs(min_value))

        # Maximal deviation from unity
        error = max_deviation - 1
        output = ROOT.TF1("fMaxDeviation", "pol0", 0, 100)
        output.SetParameter(0, error)
        return output
