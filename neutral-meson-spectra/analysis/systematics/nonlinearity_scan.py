from __future__ import print_function
import ROOT
import pytest

from spectrum.comparator import Comparator
from spectrum.options import CompositeNonlinearityScanOptions
from spectrum.options import CompositeNonlinearityOptions
from spectrum.output import open_loggs
from spectrum.tools.mc import Nonlinearity
from spectrum.tools.scan import NonlinearityScan, form_histnames
from vault.datavault import DataVault


def final_nonliearity_data(production, histname):
    return (
        DataVault().input("data", listname="Phys", histname="MassPtSM0"),
        (
            DataVault().input(production, "low", histname=histname),
            DataVault().input(production, "high", histname=histname),
        )
    )


@pytest.fixture
def nbins():
    return 9


@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.interactive
def test_scan_nonlinearities(nbins):
    prod = "single #pi^{0} nonlinearity scan"
    histnames = form_histnames(nbins)
    low = DataVault().input(prod, "low", inputs=histnames)
    high = DataVault().input(prod, "high", inputs=histnames)

    options = CompositeNonlinearityScanOptions("#pi^{0}", nbins=nbins)
    options.factor = 1.

    low, high = low.read_multiple(2), high.read_multiple(2)
    mc_data = [(l, h) for l, h in zip(low, high)]

    with open_loggs("calculating the scan") as loggs:
        chi2ndf = NonlinearityScan(options).transform(
            (
                DataVault().input("data", histname="MassPtSM0"),
                mc_data
            ),
            loggs
        )

        # TODO: Add this to the output
        ofile = ROOT.TFile("nonlinearity_scan.root", "recreate")
        chi2ndf.Write()
        ofile.Close()
        Comparator().compare(chi2ndf)


@pytest.mark.skip('')
@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.interactive
def test_draw_most_optimal_nonlinearity(nbins):
    production = "single #pi^{0} nonlinearity scan"
    minimum_index = 70
    minimum_index *= 2
    histname = form_histnames(nbins)[minimum_index]
    histname = histname[1:]  # Remove first h
    print(histname)
    # production = "single #pi^{0}"
    # histname = "MassPt"
    options = CompositeNonlinearityOptions()
    options.fitf = None
    options.factor = 1.
    estimator = Nonlinearity(options)
    with open_loggs("optimal nonlinearity") as loggs:
        nonlinearity = estimator.transform(  # noqa
            final_nonliearity_data(production, histname),
            loggs
        )
    # Comparator().compare(nonlinearity)