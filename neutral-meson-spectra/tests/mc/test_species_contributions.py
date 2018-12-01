import pytest

from spectrum.options import Options
from spectrum.analysis import Analysis
from spectrum.pipeline import ComparePipeline
from spectrum.pipeline import HistogramSelector
from spectrum.pipeline import Pipeline
from spectrum.input import SingleHistInput

from vault.datavault import DataVault


PARTICLES_SETS = {
    # "#rho^{-}", "K^{s}_{0}", "#Lambda", "#pi^{+}", "#pi^{-}", "#eta", "#omega", "K^{*+}", "K^{*-}", "K^{*0}", "#barK^{*0}", "K^{+}", "K^{-}", "#Sigma^{0}"],
    "primary": ["", "#rho^{+}", ],
    "secondary":
        ["", "K^{s}_{0}", "#Lambda", "#pi^{+}", "#pi^{-}", "#eta", "#omega"],
    "feeddown":
        ["", "K^{s}_{0}", "#Lambda", "#pi^{+}", "#pi^{-}", "#eta", "#omega"]
}


@pytest.mark.skip("debug")
@pytest.mark.onlylocal
@pytest.mark.parametrize("origin", [
    "primary",
    "secondary",
    "feeddown"
])
def test_species_contributions(origin):
    for particle in PARTICLES_SETS[origin]:
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


@pytest.mark.onlylocal
@pytest.mark.parametrize("origin", [
    "primary",
    "secondary",
    "feeddown"
])
def test_relative_contributions(origin):
    for particle in PARTICLES_SETS[origin]:
        histname = 'hPt_#pi^{0}_%s_%s' % (origin, particle)
        estimator = ComparePipeline([
            (particle, SingleHistInput(histname, "MCStudy")),
            ("#pi^0", SingleHistInput("hPt_#pi^{0}", "MCStudy")),
        ])
        inputs = DataVault().input("pythia8", listname="MCStudy")
        estimator.transform((inputs,) * 2, {})
