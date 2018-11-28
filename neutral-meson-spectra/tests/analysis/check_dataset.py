import pytest

import spectrum.comparator as cmpr
from spectrum.analysis import Analysis
from spectrum.options import Options
from spectrum.output import AnalysisOutput
from vault.datavault import DataVault


# This test is needed to check if the dataset does contain
# correct spectrum, invariant mass distribution is ok, etc.

@pytest.mark.interactive
@pytest.mark.onlylocal
@pytest.mark.parametrize("particle", ["#pi^{0}", "#eta"])
def test_dataset(particle):
    # Configure the analysis
    options = Options(particle=particle)
    options.output.scalew_spectrum = True
    estimator = Analysis(options)

    # Analyze the data
    observables = estimator.transform(
        DataVault().input('data'),
        AnalysisOutput("ALICE, \sqrt{s} = 13 TeV", "\pi^{0}")
    )

    # c1 = gcanvas(1. / 2, resize=True)
    diff = cmpr.Comparator()
    for obs in observables:
        diff.compare(obs)
