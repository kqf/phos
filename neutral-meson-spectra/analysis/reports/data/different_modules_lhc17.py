import pytest

from spectrum.analysis import Analysis
from spectrum.options import Options
from spectrum.output import open_loggs
from spectrum.pipeline import ComparePipeline
from vault.datavault import DataVault


@pytest.fixture
def data():
    return DataVault().modules_input("data", "LHC17 qa1", "Phys", True)


@pytest.mark.qa
@pytest.mark.onlylocal
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    "#eta",
])
def analyze(particle, data):
    options = Options(
        particle=particle,
        ptrange="config/test_different_modules.json"
    )
    estimator = ComparePipeline([
        ('module {0}'.format(i), Analysis(options))
        for i, _ in enumerate(data)
    ])

    with open_loggs("different modules {}".format(particle)) as loggs:
        estimator.transform(data, loggs)
