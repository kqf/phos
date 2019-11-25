import pytest

from spectrum.uncertainties.nonlinearity import _masses
from spectrum.plotter import plot


@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    # "#eta",
])
def test_nonlinearity_uncertainty(particle):
    prod = "single #pi^{0} nonlinearity scan"
    masses = _masses(prod)
    plot(
        masses,
        logy=False,
        legend_pos=None,
    )
