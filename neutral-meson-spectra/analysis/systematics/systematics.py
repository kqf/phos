import pytest
from spectrum.options import CompositeCorrectedYieldOptions
from spectrum.output import open_loggs
from spectrum.pipeline import ComparePipeline

from spectrum.uncertainties.acceptance import Acceptance,
from spectrum.uncertainties.acceptance import AcceptanceOptions
from spectrum.uncertainties.acceptance import acceptance_data

from spectrum.uncertainties.tof import TofUncertainty,
from spectrum.uncertainties.tof import TofUncertaintyOptions
from spectrum.uncertainties.tof import tof_data

from spectrum.uncertainties.gscale import GScale
from spectrum.uncertainties.gscale import GScaleOptions
from spectrum.uncertainties.gscale import ge_scale_data

from spectrum.uncertainties.nonlinearity import NonlinearityUncertainty,
from spectrum.uncertainties.nonlinearity import NonlinearityUncertaintyOptions
from spectrum.uncertainties.nonlinearity import nonlinearity_scan_data

from spectrum.uncertainties.yields import YieldExtractioin,
from spectrum.uncertainties.yields import YieldExtractioinUncertanityOptions
from spectrum.uncertainties.yields import yield_extraction_data


@pytest.fixture
def nbins():
    return 2


@pytest.fixture
def data(nbins):
    return (
        # yield_extraction_data(),
        nonlinearity_scan_data(nbins, "single #pi^{0}"),
        tof_data(),
        ge_scale_data("#pi^{0}"),
        acceptance_data(),
    )


@pytest.mark.thesis
@pytest.mark.interactive
@pytest.mark.onlylocal
def test_draws_all_sources(nbins, data):
    nonlin_options = NonlinearityUncertaintyOptions(nbins=nbins)
    nonlin_options.factor = 1.

    # cyield_options = CompositeCorrectedYieldOptions(particle="#pi^{0}")

    estimator = ComparePipeline((
        # ("yield", YieldExtractioin(
        #     YieldExtractioinUncertanityOptions(cyield_options))),
        ("nonlinearity", NonlinearityUncertainty(nonlin_options)),
        ("tof", TofUncertainty(TofUncertaintyOptions())),
        ("gescale", GScale(GScaleOptions(particle="#pi^{0}"))),
        ("accepntace", Acceptance(AcceptanceOptions(particle="#pi^{0}"))),
    ), plot=True)

    with open_loggs() as loggs:
        estimator.transform(data, loggs)
