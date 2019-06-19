import pytest

import spectrum.comparator as cmpr
from spectrum.analysis import Analysis
from spectrum.options import Options
from spectrum.output import open_loggs
from vault.datavault import DataVault


# This test is needed to check if the dataset does contain
# correct spectrum, invariant mass distribution is ok, etc.

@pytest.fixture
def data():
    return DataVault().input('data', histname="MassPtSM0")


@pytest.mark.interactive
@pytest.mark.onlylocal
@pytest.mark.parametrize("particle", ["#pi^{0}", "#eta"])
def test_dataset(particle, data):
    # Configure the analysis
    options = Options(particle=particle)
    options.output.scalew_spectrum = True
    estimator = Analysis(options)

    # Analyze the data
    with open_loggs("ALICE, #sqrt{s} = 13 TeV", "#pi^{0}") as loggs:
        observables = estimator.transform(data, loggs)
        diff = cmpr.Comparator()
        for obs in observables:
            diff.compare(obs)
