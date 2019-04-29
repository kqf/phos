import pytest
from spectrum.output import AnalysisOutput
from uncertainties.gscale import GScale, GScaleOptions, ge_scale_data
from spectrum.comparator import Comparator


@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    # "#eta",
])
def test_interface_composite(particle):
    estimator = GScale(GScaleOptions(particle=particle), plot=False)
    uncertanity = estimator.transform(
        ge_scale_data(particle),
        loggs=AnalysisOutput("test composite corr. yield interface")
    )
    Comparator().compare(uncertanity)
