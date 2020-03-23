import pytest

import spectrum.plotter as plt
from spectrum.analysis import Analysis
from spectrum.options import Options
from spectrum.output import open_loggs
from spectrum.vault import DataVault


# This test is needed to check if the dataset does contain
# correct spectrum, invariant mass distribution is ok, etc.

@pytest.fixture
def data():
    return DataVault().input('data', histname="MassPtSM0")


@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    "#eta"
])
def test_dataset(particle, data, stop):
    # Configure the analysis
    options = Options(particle=particle)
    options.output.scalew_spectrum = True
    estimator = Analysis(options)

    # Analyze the data
    with open_loggs() as loggs:
        observables = estimator.transform(data, loggs)
        for obs in observables:
            plt.plot([obs], logy=False, stop=stop)
