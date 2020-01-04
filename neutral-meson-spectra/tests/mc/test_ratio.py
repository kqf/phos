import pytest

from spectrum.analysis import Analysis
from spectrum.efficiency import Efficiency
from spectrum.pipeline import Pipeline, ComparePipeline, HistogramSelector
from spectrum.options import Options, EfficiencyOptions
from spectrum.output import open_loggs

from vault.datavault import DataVault

from spectrum.cyield import YieldRatio
from spectrum.options import CorrectedYieldOptions
from spectrum.comparator import Comparator
from spectrum.tools.feeddown import data_feeddown


@pytest.fixture
def dataset():
    return (
        DataVault().input("pythia8", listname="PhysEff"),
        DataVault().input("pythia8", listname="PhysEff")
    )


@pytest.fixture
def pt():
    return "config/pt-same.json"


@pytest.mark.skip("")
@pytest.mark.onlylocal
@pytest.mark.interactive
def test_compare_raw_yields(dataset, pt):
    estimator = ComparePipeline([
        ("#eta", Pipeline([
            ("analysis", Analysis(
                Options(particle="#eta", pt=pt))),
            ("spectrum", HistogramSelector("spectrum")),
        ])),
        ("#pi^{0}", Pipeline([
            ("analysis", Analysis(
                Options(particle="#pi^{0}", pt=pt))),
            ("spectrum", HistogramSelector("spectrum")),
        ])),
    ])
    with open_loggs("mc raw yield ratio") as loggs:
        output = estimator.transform(dataset, loggs)
        Comparator().compare(output)


@pytest.mark.skip("")
@pytest.mark.onlylocal
@pytest.mark.interactive
def test_efficiency(dataset):
    pt = "config/pt-same.json"
    estimator = ComparePipeline([
        ("#eta", Efficiency(
            EfficiencyOptions(particle="#eta", pt=pt, scale=1))),
        ("#pi^{0}", Efficiency(
            EfficiencyOptions(particle="#pi^{0}", pt=pt, scale=1))),
    ], plot=True)
    with open_loggs() as loggs:
        output = estimator.transform(dataset, loggs)
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
def options(pt):
    options_eta = CorrectedYieldOptions(particle="#eta", pt=pt)
    options_pi0 = CorrectedYieldOptions(particle="#pi^{0}", pt=pt)
    return options_eta, options_pi0


# @pytest.mark.skip("")
@pytest.mark.onlylocal
@pytest.mark.interactive
def test_yield_ratio(data, options):
    options_eta, options_pi0 = options

    estimator = YieldRatio(
        options_eta=options_eta,
        options_pi0=options_pi0,
        plot=True
    )

    with open_loggs("eta to pion ratio") as loggs:
        output = estimator.transform(data, loggs=loggs)
        Comparator().compare(output)
