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
@pytest.mark.interactive
def test_compare_raw_yields(dataset):
    ptrange = "config/pt-same.json"
    estimator = ComparePipeline([
        ("#eta", Pipeline([
            ("analysis", Analysis(
                Options(particle="#eta", ptrange=ptrange))),
            ("spectrum", HistogramSelector("spectrum")),
        ])),
        ("#pi^{0}", Pipeline([
            ("analysis", Analysis(
                Options(particle="#pi^{0}", ptrange=ptrange))),
            ("spectrum", HistogramSelector("spectrum")),
        ])),
    ])
    loggs = AnalysisOutput("raw_yield_ratio")
    output = estimator.transform(dataset, loggs)
    Comparator().compare(output)
    # loggs.plot()


# @pytest.mark.skip("")    
@pytest.mark.onlylocal
@pytest.mark.interactive
def test_efficiency(dataset):
    ptrange = "config/pt-same.json"
    estimator = ComparePipeline([
        ("#eta", Efficiency(
            EfficiencyOptions(particle="#eta", ptrange=ptrange, scale=1))),
        ("#pi^{0}", Efficiency(
            EfficiencyOptions(particle="#pi^{0}", ptrange=ptrange, scale=1))),
    ], plot=True)
    loggs = AnalysisOutput("efficiency_ratio")
    output = estimator.transform(dataset, loggs)
    loggs.plot()
    Comparator().compare(output)


@pytest.fixture
def data():

    # Define the inputs and the dataset for #eta mesons
    #
    data_eta = (
        (
            DataVault().input("pythia8", listname="PhysEff"),
            data_feeddown(dummy=True),
        ),
        DataVault().input("pythia8", listname="PhysEff")
    )

    # Define the inputs and the dataset for #pi^{0}
    #
    data_pi0 = (
        (
            DataVault().input("pythia8", listname="PhysEff"),
            data_feeddown(),
        ),
        DataVault().input("pythia8", listname="PhysEff"),
    )
    return data_eta, data_pi0


@pytest.fixture
def options():
    options_eta = CorrectedYieldOptions(particle="#eta")
    options_pi0 = CorrectedYieldOptions(particle="#pi^{0}")
    options_pi0.set_binning(
        options_eta.analysis.pt.ptedges,
        options_eta.analysis.pt.rebins
    )
    return options_eta, options_pi0


@pytest.mark.skip("")
@pytest.mark.onlylocal
@pytest.mark.interactive
def test_yield_ratio(data, options):
    options_eta, options_pi0 = options

    estimator = YieldRatio(
        options_eta=options_eta,
        options_pi0=options_pi0,
        plot=True
    )

    loggs = AnalysisOutput("eta to pion ratio")
    output = estimator.transform(data, loggs=loggs)
    Comparator().compare(output)
