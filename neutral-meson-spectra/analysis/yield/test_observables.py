import pytest

import ROOT
from spectrum.analysis import Analysis
from spectrum.broot import BROOT as br
from spectrum.options import Options
from spectrum.output import AnalysisOutput

from tools.validate import validate
from vault.datavault import DataVault


@pytest.fixture(scope="module")
def minuit_config():
    # Important:
    # This one should be set explicitely otherwise the test will fail
    # Because this global variable is set to Minuit2 in other tests
    ROOT.TVirtualFitter.SetDefaultFitter('Minuit')


def validate_particle(particle="#pi^{0}", selection="PhysTender"):
    estimator = Analysis(
        Options(particle=particle)
    )

    output = estimator.transform(
        DataVault().input("data", "stable old",
                          selection, label='testsignal'),
        AnalysisOutput("testing_the_singnal", particle)
    )
    actual = {
        h.GetName(): list(br.bins(h).contents) for h in output
    }
    validate(actual, "test_observables/{}".format(particle))


def test_extracts_pi0_spectrum(minuit_config):
    validate_particle("#pi^{0}", "PhysTender")


def test_extracts_eta_spectrum(minuit_config):
    validate_particle("#eta", "EtaTender")
