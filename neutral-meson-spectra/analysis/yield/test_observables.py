import pytest

import ROOT
from spectrum.analysis import Analysis
from spectrum.broot import BROOT as br
from spectrum.options import Options
from spectrum.output import open_loggs

from spectrum.tools.validate import validate
from vault.datavault import DataVault


@pytest.fixture(scope="module")
def minuit_config():
    # Important:
    # This one should be set explicitely otherwise the test will fail
    # Because this global variable is set to Minuit2 in other tests
    ROOT.TVirtualFitter.SetDefaultFitter('Minuit')


def data(selection):
    return DataVault().input("data", "stable old", selection, label='test')


@pytest.mark.parametrize(("particle, selection"), [
    ("#pi^{0}", "PhysTender"),
    ("#eta", "EtaTender"),
])
def test_extracts_spectrum(particle, selection, minuit_config):
    with open_loggs("signal {}".format(particle)) as loggs:
        output = Analysis(Options(particle=particle)).transform(
            data(selection),
            loggs
        )

    actual = {
        h.GetName(): list(br.bins(h).contents) for h in output
    }
    validate(actual, "test_observables/{}".format(particle))
    # validate_particle(particle, dataset)
