import joblib
from collections import namedtuple
from multimethod import multimethod

import spectrum.broot as br
from spectrum.pipeline import TransformerBase
from spectrum.pipeline import ReducePipeline
from spectrum.pipeline import ParallelPipeline
from spectrum.pipeline import RebinTransformer
from spectrum.output import open_loggs
from spectrum.constants import cross_section

from spectrum.cyield import CorrectedYield, cyield_data
from spectrum.options import CompositeCorrectedYieldOptions

from spectrum.uncertainties.total import TotalUncertainty, data_total_uncert
from spectrum.uncertainties.total import TotalUncertaintyOptions


def data_spectrum(particle):
    return (
        cyield_data(particle),
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
        spectrum.SetTitle("Data")
        spectrum.Scale(cross_section())
        statistics = spectrum.Clone("statistics")
        systematics = spectrum.Clone("systematics")

        absolute_error = (
            br.bins(spectrum).contents * br.bins(uncertainty).contents
        )

        for i in br.hrange(systematics):
            systematics.SetBinError(i, absolute_error[i - 1])

        total_errors = (
            br.bins(statistics).errors ** 2 + br.bins(systematics).errors ** 2
        ) ** 0.5

        for i in br.hrange(spectrum):
            spectrum.SetBinError(i, total_errors[i - 1])

        t = namedtuple("Production", ["spectrum", "statistics", "systematics"])
        return t(spectrum, statistics, systematics)


memory = joblib.Memory(".joblib-cachedir", verbose=0)


@memory.cache()
def spectrum(particle):
    data = data_spectrum(particle=particle)
    estimator = Spectrum(particle=particle)
    with open_loggs() as loggs:
        output = estimator.transform(data, loggs)
    return br.PhysicsHistogram(*output)


def ratio(stop=False):
    pion = spectrum("#pi^{0}")
    eta = spectrum("#eta")
    with open_loggs() as loggs:
        pion = RebinTransformer(True, br.edges(eta.tot)).transform(pion, loggs)
    ratio = br.ratio(eta, pion)
    ratio.SetTitle("#eta / #pi^{0}; #it{p}_T (GeV/#it{c}); #eta / #pi^{0}")
    return ratio


class DataExtractor(TransformerBase):
    @multimethod
    def transform(self, info, loggs):
        return br.from_hepdata(info)

    @transform.register(TransformerBase, str)
    def _(self, particle, loggs):
        hist = spectrum(particle)
        hist.energy = 13000
        hist.SetTitle("pp, #sqrt{#it{s}} = 13 TeV")
        return hist
