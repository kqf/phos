import pytest
from spectrum.output import AnalysisOutput
from uncertainties.acceptance import Acceptance, AcceptanceOptions
from uncertainties.acceptance import acceptance_data
from spectrum.comparator import Comparator


@pytest.mark.thesis
@pytest.mark.interactive
@pytest.mark.onlylocal
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    # "#eta"
])
def test_acceptance(particle):
    estimator = Acceptance(
        AcceptanceOptions(particle=particle), plot=False)
    loggs = AnalysisOutput("uncertainty acceptance")
    uncertanity = estimator.transform(
        acceptance_data(particle),
        loggs=loggs
    )
    Comparator().compare(uncertanity)
    loggs.plot()
