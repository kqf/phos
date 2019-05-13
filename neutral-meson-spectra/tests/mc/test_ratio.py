import pytest

from spectrum.analysis import Analysis
from spectrum.efficiency import Efficiency
from spectrum.pipeline import Pipeline, ComparePipeline, HistogramSelector
from spectrum.options import Options, EfficiencyOptions
from spectrum.output import AnalysisOutput

from vault.datavault import DataVault

from spectrum.corrected_yield import YieldRatio
from spectrum.options import CorrectedYieldOptions
from spectrum.comparator import Comparator
from tools.feeddown import data_feeddown


@pytest.fixture
def dataset():
    return (
        DataVault().input("pythia8", listname="PhysEff"),
        DataVault().input("pythia8", listname="PhysEff")
    )


@pytest.mark.skip("")
@pytest.mark.onlylocal
def test_compare_raw_yields(dataset):
    ptrange = "config/pt-same.json"
    estimator = ComparePipeline([
        ("#eta", Pipeline([
            ("analysis", Analysis(
                Options(particle="#pi^{0}", ptrange=ptrange))),
            ("spectrum", HistogramSelector("spectrum")),
        ])),
        ("#pi^{0}", Pipeline([
            ("analysis", Analysis(Options(particle="#eta", ptrange=ptrange))),
            ("spectrum", HistogramSelector("spectrum")),
        ])),
    ])
    loggs = AnalysisOutput("raw_yield_ratio")
    estimator.transform(dataset, loggs)
    loggs.plot()


@pytest.mark.skip("")
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
    data_eta = (
        (
            DataVault().input("pythia8", listname="PhysEff"),
            data_feeddown(dummy=True),
        ),
        DataVault().input("pythia8", listname="PhysEff")
    )

    options_eta = CorrectedYieldOptions(particle="#eta")

    # Define the inputs and the dataset for #pi^{0}
    #
    data_pi0 = (
        (
            DataVault().input("pythia8", listname="PhysEff"),
            data_feeddown(),
        ),
        DataVault().input("pythia8", listname="PhysEff"),
    )

    options_pi0 = CorrectedYieldOptions(particle="#pi^{0}")
    # Make same binning for all neutral mesons
    options_pi0.set_binning(
        options_eta.analysis.pt.ptedges,
        options_eta.analysis.pt.rebins
    )
    return data_eta, options_eta, data_pi0, options_pi0


@pytest.mark.skip("")
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
