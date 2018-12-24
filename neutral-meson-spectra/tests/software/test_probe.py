import pytest

from lazy_object_proxy import Proxy
from tools.probe import TagAndProbe
from vault.datavault import DataVault
from spectrum.options import ProbeTofOptions
from spectrum.output import AnalysisOutput


DATASET = Proxy(
    lambda: (
        DataVault().input("data", "uncorrected", "TagAndProbleTOFOnlyTender",
                          histname="MassEnergyTOF_SM0"),
        DataVault().input("data", "uncorrected", "TagAndProbleTOFOnlyTender",
                          histname="MassEnergyAll_SM0"),
    ),
)


@pytest.mark.onlylocal
def test_interface():
    probe = TagAndProbe(ProbeTofOptions())
    eff = probe.transform(
        DATASET,
        loggs=AnalysisOutput("Test the tag and probe interface")
    )
    assert eff.GetEntries() > 0
