from spectrum.pipeline import TransformerBase
from spectrum.pipeline import ReducePipeline
from spectrum.pipeline import ParallelPipeline
from spectrum.broot import BROOT as br


from spectrum.corrected_yield import CorrectedYield, data_cyield
from spectrum.options import CompositeCorrectedYieldOptions

from spectrum.uncertainties.total import TotalUncertainty, data_total_uncert
from spectrum.uncertainties.total import TotalUncertaintyOptions


def data_spectrum(particle):
    return (
        data_cyield(particle),
        data_total_uncert(particle)
    )


class Spectrum(TransformerBase):
    def __init__(self, particle="#pi^{0}", plot=False):
        cyield = CorrectedYield(
            CompositeCorrectedYieldOptions(particle=particle))

        uncert = TotalUncertainty(TotalUncertaintyOptions(particle))
        self.pipeline = ReducePipeline(
            ParallelPipeline([
                ("corrected yield", cyield),
                ("uncertainties", uncert),
            ]),
            self.reduce)

    def reduce(self, data, loggs):
        spectrum, uncertainty = data
        statistics = spectrum.Clone("statistics")
        systematics = spectrum.Clone("systematics")

        absolute_error = (
            br.bins(spectrum).contents * br.bins(uncertainty).contents
        )

        for i in br.range(systematics):
            systematics.SetBinError(i, absolute_error[i - 1])

        total_errors = (
            br.bins(statistics).errors ** 2 + br.bins(uncertainty).errors ** 2
        ) ** 0.5

        for i in br.range(spectrum):
            spectrum.SetBinError(i, total_errors[i - 1])

        return spectrum, statistics, systematics
