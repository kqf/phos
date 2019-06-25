import pytest

from spectrum.output import AnalysisOutput
from spectrum.pipeline import ComparePipeline

from spectrum.options import CompositeCorrectedYieldOptions

from uncertainties.nonlinearity import CompositeNonlinearityUncertaintyOptions
from uncertainties.yields import YieldExtractioin, yield_extraction_data
from uncertainties.yields import YieldExtractioinUncertanityOptions
from uncertainties.nonlinearity import Nonlinearity, nonlinearity_scan_data
from uncertainties.tof import TofUncertainty, TofUncertaintyOptions
from uncertainties.tof import tof_data
from uncertainties.gscale import GScale, GScaleOptions, ge_scale_data
from uncertainties.acceptance import Acceptance, AcceptanceOptions
from uncertainties.acceptance import acceptance_data


def data(nbins):
    return (
        yield_extraction_data(),
        nonlinearity_scan_data(nbins, "single #pi^{0}"),
        tof_data(),
        ge_scale_data(),
        acceptance_data(),
    )


@pytest.mark.thesis
@pytest.mark.interactive
@pytest.mark.onlylocal
def test_draws_all_sources():
    nbins = 2
    nonlin_options = CompositeNonlinearityUncertaintyOptions(nbins=nbins)
    nonlin_options.factor = 1.

    cyield_options = CompositeCorrectedYieldOptions(particle="#pi^{0}")

    estimator = ComparePipeline((
        ("yield", YieldExtractioin(
            YieldExtractioinUncertanityOptions(cyield_options))),
        ("nonlinearity", Nonlinearity(nonlin_options)),
        ("tof", TofUncertainty(TofUncertaintyOptions())),
        ("gescale", GScale(GScaleOptions(particle="#pi^{0}"))),
        ("accepntace", Acceptance(AcceptanceOptions(particle="#pi^{0}"))),
    ), plot=True)

    loggs = AnalysisOutput("testing the scan interface")
    estimator.transform(data(nbins), loggs)
    loggs.plot(True)
