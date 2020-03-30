import pytest

from spectrum.tools.probe import TagAndProbe, tof_data
from spectrum.options import ProbeTofOptions
from spectrum.output import open_loggs


@pytest.fixture
def data():
    return tof_data()


@pytest.mark.onlylocal
def test_interface(data):
    with open_loggs() as loggs:
        probe = TagAndProbe(ProbeTofOptions())
        eff = probe.transform(data, loggs)
    assert eff.GetEntries() > 0
