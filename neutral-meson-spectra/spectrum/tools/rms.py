from spectrum.pipeline import TransformerBase
import spectrum.broot as br


class RmsToMean(TransformerBase):
    def __init__(self, options, plot):
        super(RmsToMean, self).__init__(plot)
        self.options = options

    def transform(self, histograms, loggs):
        mean = br.average(histograms, "average")
        ratios = [br.ratio(h, mean, "") for h in histograms]
        average_ratio = br.average(ratios, "average_ratio")

        uncertainty = br.copy(mean)
        for i in br.hrange(uncertainty):
            uncertainty.SetBinContent(
                i,
                average_ratio.GetBinError(i) / average_ratio.GetBinContent(i)
            )
            uncertainty.SetBinError(i, 0)
        return uncertainty
