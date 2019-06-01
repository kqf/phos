import pytest

from spectrum.broot import BROOT as br
from spectrum.comparator import Comparator
from spectrum.efficiency import Efficiency
from spectrum.options import CompositeEfficiencyOptions
from spectrum.output import open_loggs
from spectrum.pipeline import ParallelPipeline, Pipeline
from spectrum.pipeline import TransformerBase
from tools.scan import NonlinearityParamExtractor, form_histnames
from vault.datavault import DataVault


class OverlapParamExtractor(NonlinearityParamExtractor):

    def read_labels(self, data):
        output = []
        for d in data:
            high, low = d
            real, mixing = low.transform()
            output.append(
                map(float, real.GetTitle().split())
            )
        return output


class OverlapNonlinearityScan(TransformerBase):
    def __init__(self, options, nbins, chi2_=br.chi2ndf, plot=True):
        super(OverlapNonlinearityScan, self).__init__()
        chi2 = ParallelPipeline([
            ("efficiency" + str(i), Efficiency(options))
            for i in range(nbins ** 2)
        ])

        extractor = OverlapParamExtractor()
        self.pipeline = Pipeline([
            ("read-titles", extractor),
            ("chi2", chi2),
            ("dump", extractor)
        ])


def add_arguments(identity, original):
    identity.filename = original.filename
    identity.histname = original.histname
    identity.listname = "PhysEff"
    identity.events = original.events
    identity.label = original.label
    return identity


def reduce_chi2(hists):
    data, mc = hists
    Comparator().compare(data, mc)
    return br.chi2(data, mc, (5, 7)) / 6


@pytest.fixture
def nbins():
    return 9


@pytest.fixture
def data(nbins):
    prod = "single #pi^{0} nonlinearity scan"
    histnames = form_histnames(nbins)
    low = DataVault().input(prod, "low", inputs=histnames)
    high = DataVault().input(prod, "high", inputs=histnames)

    low_, high_ = low.read_multiple(2), high.read_multiple(2)
    low_ = [add_arguments(l, low) for l in low_]
    high_ = [add_arguments(l, high) for l in high_]
    mc_data = [(l, h) for l, h in zip(low_, high_)]
    return mc_data


@pytest.mark.skip("")
@pytest.mark.onlylocal
@pytest.mark.interactive
def test_calculates_overlap(data):
    options = CompositeEfficiencyOptions("#pi^{0}")
    options.reduce_function = reduce_chi2

    with open_loggs("testing the scan interface") as loggs:
        estimator = OverlapNonlinearityScan(options, nbins)

        chi2ndf = estimator.transform(data, loggs)
        Comparator().compare(chi2ndf)


@pytest.fixture
def optimum(nbins, minimum_index=33):
    minimum_index = 33
    minimum_index *= 2
    histnames = form_histnames(nbins)[minimum_index: minimum_index + 2]

    prod = "single #pi^{0} nonlinearity scan"
    low = DataVault().input(prod, "low", inputs=histnames)
    high = DataVault().input(prod, "high", inputs=histnames)

    low_, high_ = low.read_multiple(2), high.read_multiple(2)
    low_ = [add_arguments(l, low) for l in low_]
    high_ = [add_arguments(l, high) for l in high_]
    return [(l, h) for l, h in zip(low_, high_)]


@pytest.mark.onlylocal
@pytest.mark.interactive
def test_optimum(nbins, optimum):
    options = CompositeEfficiencyOptions("#pi^{0}")
    options.reduce_function = reduce_chi2

    with open_loggs("testing the scan interface") as loggs:
        chi2ndf = OverlapNonlinearityScan(options, 1).transform(optimum, loggs)
        Comparator().compare(chi2ndf)
