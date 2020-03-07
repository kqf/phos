import pytest
import json
import six

import spectrum.plotter as plt
from spectrum.vault import FVault
from spectrum.spectra import energies


def tsallis(parameters):
    fitf = FVault().tf1("tsallis")
    for i, p in enumerate(parameters):
        fitf.FixParameter(i, p)
    return fitf


@pytest.fixture
def parameters(particle):
    with open("config/predictions/tsallis.json") as f:
        data = json.load(f)[particle]
    pars = {
        label: [v["A"], v["C"], v["n"], v["M"]]
        for label, v in six.iteritems(data)
    }
    return pars


@pytest.fixture
def data(particle):
    return energies(particle)


@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    "#eta",
])
def test_downloads_from_hepdata(data, parameters):
    for spectrum, pars in zip(data, parameters.values()):
        fitf = tsallis(pars)
        spectrum.Fit(fitf)
        plt.plot([spectrum, fitf])
