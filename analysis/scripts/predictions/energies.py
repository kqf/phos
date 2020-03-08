import pytest

import spectrum.plotter as plt
from spectrum.output import open_loggs
from spectrum.pipeline import SingleHistReader
from spectrum.vault import DataVault

from spectrum.spectra import energies


@pytest.fixture
def theory_data():
    return DataVault().input("theory", "7 TeV", histname="#sigma_{total}")


@pytest.fixture
def theory(theory_data):
    with open_loggs() as loggs:
        data = SingleHistReader().transform(theory_data, loggs)
    return data


@pytest.fixture
def data(particle):
    return sorted(energies(particle), key=lambda x: x.energy)


@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("particle", ["#pi^{0}", "#eta"])
def test_downloads_from_hepdata(data, theory):
    plt.plot(data + [theory])
