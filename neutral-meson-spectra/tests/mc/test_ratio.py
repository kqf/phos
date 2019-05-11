import pytest

from spectrum.analysis import Analysis
from spectrum.efficiency import Efficiency
from spectrum.pipeline import Pipeline, ComparePipeline, HistogramSelector
from spectrum.options import Options, EfficiencyOptions
from spectrum.output import AnalysisOutput

from vault.datavault import DataVault

from spectrum.corrected_yield import YieldRatio, CorrectedYield
from spectrum.options import CompositeCorrectedYieldOptions
from spectrum.comparator import Comparator
from tools.feeddown import data_feeddown


@pytest.fixture
def dataset():
    return (
        DataVault().input("pythia8", listname="PhysEff"),
        DataVault().input("pythia8", listname="PhysEff")
    )


@pytest.mark.onlylocal
def test_compare_raw_yields(dataset):
    ptrange = "config/pt-same.json"
    estimator = ComparePipeline([
        ("#pi^{0}", Pipeline([
            "analysis", Analysis(Options(particle="#eta", ptrange=ptrange)),
            "spectrum", HistogramSelector("spectrum")
        ])),
        ("#eta", Pipeline([
            "analysis", Analysis(Options(particle="#pi^{0}", ptrange=ptrange)),
            "spectrum", HistogramSelector("spectrum")
        ])),
    ])
    loggs = AnalysisOutput("raw_yield_ratio")
    estimator.transform(dataset, loggs)
    loggs.plot()


@pytest.mark.onlylocal
def test_efficiency(dataset):
    ptrange = "config/pt-same.json"
    estimator = ComparePipeline([
        ("#pi^{0}", Efficiency(
            EfficiencyOptions(particle="#eta", ptrange=ptrange))),
        ("#eta", Efficiency(
            EfficiencyOptions(particle="#pi^{0}", ptrange=ptrange))),
    ])
    loggs = AnalysisOutput("efficiency_ratio")
    estimator.transform(dataset, loggs)
    loggs.plot()


@pytest.fixture
def ratio_inputs():

    # Define the inputs and the dataset for #eta mesons
    #
    inputs_eta = (
        DataVault().input("single #eta", "low"),
        DataVault().input("single #eta", "high"),
    )

    data_eta = (
        (
            DataVault().input("data", histname="MassPtSM0"),
            data_feeddown(dummy=True),
        ),
        inputs_eta
    )

    options_eta = CompositeCorrectedYieldOptions(particle="#eta")

    # Define the inputs and the dataset for #pi^{0}
    #
    prod = "single #pi^{0}"
    inputs_pi0 = (
        DataVault().input(prod, "low", "PhysEff"),
        DataVault().input(prod, "high", "PhysEff"),
    )

    data_pi0 = (
        (
            DataVault().input("data", histname="MassPtSM0"),
            data_feeddown(),
        ),
        inputs_pi0
    )

    options_pi0 = CompositeCorrectedYieldOptions(particle="#pi^{0}")
    # Make same binning for all neutral mesons
    options_pi0.set_binning(
        options_eta.analysis.pt.ptedges,
        options_eta.analysis.pt.rebins
    )
    return data_eta, options_eta, data_pi0, options_pi0


@pytest.mark.onlylocal
def test_yield_ratio(ratio_inputs):
    data_eta, options_eta, data_pi0, options_pi0 = ratio_inputs

    estimator = YieldRatio(
        options_eta=options_eta,
        options_pi0=options_pi0,
        plot=True
    )

    loggs = AnalysisOutput("eta to pion ratio")
    output = estimator.transform(
        (data_eta, data_pi0),
        loggs=loggs
    )
    Comparator().compare(output)
