import pytest

import ROOT
from spectrum.analysis import Analysis
import spectrum.broot as br
from spectrum.options import Options
from spectrum.output import open_loggs

from spectrum.tools.validate import validate
from spectrum.vault import DataVault


@pytest.fixture(scope="module")
def minuit_config():
    # Important:
    # This one should be set explicitely otherwise the test will fail
    # Because this global variable is set to Minuit2 in other tests
    ROOT.TVirtualFitter.SetDefaultFitter('Minuit')


@pytest.fixture
def data(selection):
    return DataVault().input("data", "stable", selection)


@pytest.mark.onlylocal
@pytest.mark.parametrize(("particle, selection"), [
    ("#pi^{0}", "Phys"),
    ("#eta", "Eta"),
])
def test_extracts_spectrum(particle, selection, data, minuit_config):
    with open_loggs() as loggs:
        output = Analysis(Options(particle=particle)).transform(data, loggs)

    for h in output:
        name = h.GetName()
        path = "test_observables/{}/{}".format(particle, name)
        print(path)
        validate(br.hist2dict(h), path)
