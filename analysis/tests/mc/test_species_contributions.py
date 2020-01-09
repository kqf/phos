import json
import pytest

from spectrum.options import Options
from spectrum.analysis import Analysis
from spectrum.pipeline import ComparePipeline
from spectrum.pipeline import HistogramSelector
from spectrum.pipeline import Pipeline
from spectrum.pipeline import SingleHistReader
from spectrum.output import open_loggs

from spectrum.vault import DataVault


@pytest.fixture
def particles(origin):
    with open("config/test_species.json") as f:
        return json.load(f)[origin]


@pytest.mark.skip
@pytest.mark.onlylocal
@pytest.mark.parametrize("origin", [
    "primary",
    "secondary",
    "feeddown"
])
def test_species_contributions(origin, particles):
    for particle in particles:
        estimator = ComparePipeline([
            (particle, Pipeline([
                ("analysis", Analysis(Options())),
                ("spectrum", HistogramSelector("spectrum")),
            ])),
            ("#pi^0", SingleHistReader()),
        ])
        data = (
            DataVault().input(
                "pythia8",
                listname="MCStudy",
                histname="MassPt_#pi^{{0}}_{}_{}".format(origin, particle),
            ),
            DataVault().input(
                "pythia8",
                listname="MCStudy",
                histname="hPt_#pi^{0}",
            )
        )
        with open_loggs() as loggs:
            estimator.transform(data, loggs)


@pytest.fixture
def data(origin, particles):
    selections = []
    for particle in particles:
        hname = "hPt_#pi^{{0}}_{}_{}".format(origin, particle)
        selections.append((
            DataVault().input("pythia8", listname="MCStudy", histname=hname),
            DataVault().input("pythia8", listname="MCStudy", histname="hPt_#pi^{0}"),  # noqa
        ))
    return selections


@pytest.mark.onlylocal
@pytest.mark.parametrize("origin", [
    "primary",
    "secondary",
    "feeddown"
])
def test_relative_contributions(origin, data, particles):
    for selection, particle in zip(data, particles):
        estimator = ComparePipeline([
            (particle, SingleHistReader()),
            ("#pi^0", SingleHistReader()),
        ], plot=False)
        msg = "{} {} distribution".format(origin, particle)
        with open_loggs(msg) as loggs:
            estimator.transform(selection, loggs)
