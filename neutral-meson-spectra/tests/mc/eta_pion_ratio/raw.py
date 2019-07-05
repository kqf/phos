import pytest

from spectrum.efficiency import Efficiency
from spectrum.pipeline import ComparePipeline
from spectrum.options import EfficiencyOptions, CompositeEfficiencyOptions
from spectrum.options import Options, CorrectedYieldOptions
from spectrum.output import open_loggs
from spectrum.corrected_yield import YieldRatio
from tools.feeddown import data_feeddown

from vault.datavault import DataVault
from spectrum.comparator import Comparator

from spectrum.analysis import Analysis
from spectrum.pipeline import TransformerBase
from spectrum.pipeline import Pipeline, HistogramSelector


@pytest.fixture
def pythia():
    return DataVault().input("pythia8", "fake", listname="PhysEff")


@pytest.fixture
def data():
    return DataVault().input("data", histname="MassPtSM0")


class RawSpectrum(TransformerBase):
    def __init__(self, options, plot=False):
        super(RawSpectrum, self).__init__()
        self.pipeline = Pipeline([
            ("analysis", Analysis(options, plot)),
            ("spectrum", HistogramSelector("spectrum"))
        ])


@pytest.mark.skip("")
@pytest.mark.onlylocal
@pytest.mark.interactive
def test_raw_yield_ratio(pythia, data):
    ptrange = "config/pt-same.json"

    def estimator():
        return ComparePipeline([
            ("#eta", RawSpectrum(
                Options(particle="#eta", ptrange=ptrange))),
            ("#pi^{0}", RawSpectrum(
                Options(particle="#pi^{0}", ptrange=ptrange))),
        ], plot=True)

    with open_loggs() as loggs:
        pythia_ratio = estimator().transform((pythia, pythia), loggs)

    with open_loggs() as loggs:
        data_ratio = estimator().transform((data, data), loggs)

    Comparator(labels=["data", "pythia"]).compare(data_ratio, pythia_ratio)


@pytest.fixture
def options():
    options_eta = CorrectedYieldOptions(particle="#eta")
    options_pi0 = CorrectedYieldOptions(particle="#pi^{0}")
    # Make same binning for all neutral mesons
    options_pi0.set_binning(
        options_eta.analysis.pt.ptedges,
        options_eta.analysis.pt.rebins
    )
    return options_eta, options_pi0


@pytest.fixture
def data_eta(pythia):
    # Define the inputs and the dataset for #eta mesons
    #
    data = (
        (
            DataVault().input("data", histname="MassPtSM0"),
            data_feeddown(dummy=True),
        ),
        pythia
    )
    return data


@pytest.fixture
def data_pion(pythia):
    data = (
        (
            DataVault().input("data", histname="MassPtSM0"),
            data_feeddown(),
        ),
        pythia
    )
    return data


@pytest.fixture
def dataset(data_eta, data_pion):
    return data_eta, data_pion


@pytest.mark.onlylocal
@pytest.mark.interactive
def test_yield_ratio(dataset, options):
    options_eta, options_pi0 = options

    estimator = YieldRatio(
        options_eta=options_eta,
        options_pi0=options_pi0,
        plot=True
    )

    with open_loggs() as loggs:
        output = estimator.transform(dataset, loggs)
    Comparator().compare(output)


@pytest.mark.skip("")
@pytest.mark.onlylocal
@pytest.mark.interactive
def test_spmc_efficiency(pythia, spmc):
    ptrange = "config/pt-same.json"

    # Now the similar code for SPMC
    estimator = ComparePipeline([
        ("#eta", Efficiency(
            CompositeEfficiencyOptions(particle="#eta", ptrange=ptrange,
                                       scale=1))),
        ("#pi^{0}", Efficiency(
            CompositeEfficiencyOptions(particle="#pi^{0}", ptrange=ptrange,
                                       scale=1))),
    ], plot=True)
    with open_loggs() as loggs:
        estimator.transform(spmc, loggs)


@pytest.mark.skip("")
@pytest.mark.onlylocal
@pytest.mark.interactive
def test_pion_efficiency(pythia, spmc):
    ptrange = "config/pt-same.json"

    estimator = Efficiency(
        EfficiencyOptions(particle="#eta", ptrange=ptrange, scale=1))

    with open_loggs("test eta pythia efficiency") as loggs:
        estimator.transform(pythia[1], loggs)
