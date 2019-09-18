import pytest
from spectrum.options import CompositeCorrectedYieldOptions
from spectrum.output import open_loggs
from spectrum.pipeline import ComparePipeline

from spectrum.uncertainties.acceptance import Acceptance
from spectrum.uncertainties.acceptance import AcceptanceOptions
from spectrum.uncertainties.acceptance import acceptance_data

from spectrum.uncertainties.tof import TofUncertainty
from spectrum.uncertainties.tof import TofUncertaintyOptions
from spectrum.uncertainties.tof import tof_data

from spectrum.uncertainties.gscale import GScale
from spectrum.uncertainties.gscale import GScaleOptions
from spectrum.uncertainties.gscale import ge_scale_data

from spectrum.uncertainties.nonlinearity import NonlinearityUncertainty
from spectrum.uncertainties.nonlinearity import NonlinearityUncertaintyOptions
from spectrum.uncertainties.nonlinearity import nonlinearity_scan_data

from spectrum.uncertainties.yields import YieldExtractioin
from spectrum.uncertainties.yields import YieldExtractioinUncertanityOptions
from spectrum.uncertainties.yields import yield_extraction_data


from spectrum.uncertainties.feeddown import FeedDown
from spectrum.uncertainties.feeddown import FeedDownOptions
from spectrum.uncertainties.feeddown import feeddown_data

from spectrum.uncertainties.material import MaterialBudget
from spectrum.uncertainties.material import MaterialBudgetOptions
from spectrum.uncertainties.material import material_budget_data


@pytest.fixture
def nbins():
    return 2


@pytest.fixture
def data(nbins):
    return (
        yield_extraction_data(),
        nonlinearity_scan_data(nbins, "single #pi^{0}"),
        tof_data(),
        ge_scale_data("#pi^{0}"),
        acceptance_data(),
        feeddown_data(),
        material_budget_data(),
    )


@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.interactive
def test_draws_all_sources(nbins, data):
    nonlin_options = NonlinearityUncertaintyOptions(nbins=nbins)
    nonlin_options.factor = 1.

    estimator = ComparePipeline((
        ("yield", YieldExtractioin(
            YieldExtractioinUncertanityOptions(particle="#pi^{0}"))),
        ("nonlinearity", NonlinearityUncertainty(nonlin_options)),
        ("tof", TofUncertainty(TofUncertaintyOptions())),
        ("gescale", GScale(GScaleOptions(particle="#pi^{0}"))),
        ("accepntace", Acceptance(AcceptanceOptions(particle="#pi^{0}"))),
        ("feed down", FeedDown(FeedDownOptions(particle="#pi^{0}"))),
        ("material budget", MaterialBudget(
            MaterialBudgetOptions(particle="#pi^{0}")))
    ), plot=True)

    with open_loggs() as loggs:
        estimator.transform(data, loggs)
