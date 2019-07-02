import pytest

from spectrum.analysis import Analysis
from spectrum.efficiency import Efficiency
from spectrum.pipeline import Pipeline, ComparePipeline, HistogramSelector
from spectrum.options import Options, EfficiencyOptions
from spectrum.output import open_loggs

from vault.datavault import DataVault

from spectrum.corrected_yield import YieldRatio
from spectrum.options import CorrectedYieldOptions
from spectrum.comparator import Comparator
from tools.feeddown import data_feeddown

from spectrum.input import SingleHistInput
from spectrum.pipeline import TransformerBase


@pytest.fixture
def dataset():
    return (
        DataVault().input("pythia8", listname="PhysEff"),
        DataVault().input("pythia8", listname="PhysEff")
    )


class EtaPionRatio(TransformerBase):
    def __init__(self, options=None, plot=False):
        super(EtaPionRatio, self).__init__()
        self.pipeline = ComparePipeline([
            ("#eta", SingleHistInput("hPt_#eta_primary_standard")),
            ("#pi^{0}", SingleHistInput("hPt_#pi^{0}_primary_standard")),
        ], plot)


@pytest.mark.onlylocal
@pytest.mark.interactive
def test_calculate_eta_pion_ratio(dataset):
    with open_loggs("eta pion ratio generated") as loggs:
        ratio = EtaPionRatio().transform(dataset, loggs)
        Comparator().compare(ratio)


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
    with open_loggs("mc raw yield ratio") as loggs:
        output = estimator.transform(dataset, loggs)
        Comparator().compare(output)


@pytest.mark.skip("")
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
def options():
    options_eta = CorrectedYieldOptions(particle="#eta")
    options_pi0 = CorrectedYieldOptions(particle="#pi^{0}")
    options_pi0.set_binning(
        options_eta.analysis.pt.ptedges,
        options_eta.analysis.pt.rebins
    )
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
