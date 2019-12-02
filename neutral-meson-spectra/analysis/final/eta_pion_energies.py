import pytest
import pandas as pd
import spectrum.broot as br
from spectrum.plotter import plot


@pytest.fixture
def data():
    raw = pd.read_json("config/physics/eta_pion_energies.json")
    return br.graph(
        "; p_{T} (GeV/#it{c}); #eta/#pi^{0}",
        raw["energy"],
        raw["eta_pion"],
        dy=raw["eta_pion_err"])


def test_reports_energies(data):
    plot(
        [data],
        logy=False,
        legend_pos=None,
        ylimits=(0, 1),
        csize=(126, 126),
    )
