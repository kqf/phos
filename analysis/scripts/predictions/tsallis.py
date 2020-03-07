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
def parameters():
    with open("config/predictions/tsallis.json") as f:
        data = json.load(f)["#pi^{0}"]
    pars = {
        label: [v["A"], v["C"], v["n"], v["M"]]
        for label, v in six.iteritems(data)
    }
    return pars


@pytest.fixture
def data():
    return energies("#pi^{0}")


@pytest.mark.onlylocal
@pytest.mark.interactive
def test_downloads_from_hepdata(data, parameters):
    for spectrum, pars in zip(data, parameters.values()):
        fitf = tsallis(pars)
        spectrum.Fit(fitf)
        plt.plot([spectrum, fitf])
