import json
import pytest

from spectrum.options import Options
from spectrum.analysis import Analysis
from spectrum.pipeline import ComparePipeline
from spectrum.pipeline import HistogramSelector
from spectrum.pipeline import Pipeline
from spectrum.input import SingleHistInput
from spectrum.output import open_loggs

from vault.datavault import DataVault


@pytest.fixture
def particles():
    with open("config/test_species.json") as f:
        return json.load(f)


@pytest.mark.onlylocal
@pytest.mark.parametrize("origin", [
    "primary",
    "secondary",
    "feeddown"
])
def test_species_contributions(origin, particles):
    for particle in particles[origin]:
        estimator = ComparePipeline([
            (particle, Pipeline([
                ("analysis", Analysis(Options())),
                ("spectrum", HistogramSelector("spectrum")),
            ])),
            ("#pi^0", SingleHistInput("hPt_#pi^{0}", "MCStudy")),
        ])
        histname = "MassPt_#pi^{0}_%s_%s" % (origin, particle)
        inputs = DataVault().input("pythia8",
                                   listname="MCStudy",
                                   histname=histname,
                                   use_mixing=False)
        estimator.transform((inputs,) * 2, {})


@pytest.fixture
def data():
    return (
        DataVault().input("pythia8", listname="MCStudy"),
        DataVault().input("pythia8", listname="MCStudy"),
    )


@pytest.mark.onlylocal
@pytest.mark.parametrize("origin", [
    "primary",
    "secondary",
    "feeddown"
])
def test_relative_contributions(origin, data, particles):
    for particle in particles[origin]:
        histname = 'hPt_#pi^{0}_%s_%s' % (origin, particle)
        estimator = ComparePipeline([
            (particle, SingleHistInput(histname, "MCStudy")),
            ("#pi^0", SingleHistInput("hPt_#pi^{0}", "MCStudy")),
        ])
        msg = "{} {} distribution".format(origin, particle)
        with open_loggs(msg) as loggs:
            estimator.transform(data, loggs)
