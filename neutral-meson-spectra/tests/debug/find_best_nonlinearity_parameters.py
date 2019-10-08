import pytest
import ROOT
import spectrum.sutils as su
import spectrum.broot as br
from spectrum.comparator import Comparator
from spectrum.options import CompositeNonlinearityScanOptions
from spectrum.output import open_loggs
from spectrum.tools.scan import NonlinearityScan, form_histnames
from vault.datavault import DataVault


def chi2(mc, data):
    def function(x, p):
        index = mc.FindBin(x[0])
        return mc.GetBinContent(index) * p[0]

    fitfunc = ROOT.TF1("testfunc", function, 0, 20, 1)
    fitfunc.SetParameter(0, 1.)
    fitfunc.SetParLimits(0, 0.5, 1.5)
    data.Fit(fitfunc, '0q')
    mc.Scale(fitfunc.GetParameter(0))
    return br.chi2ndf(mc, data)


@pytest.fixture
def nbins():
    return 9


@pytest.fixture
def mc_data(nbins):

    def multiple(part, n_hisits=2):
        prod = "single #pi^{0} nonlinearity scan"
        histnames = form_histnames(nbins)
        data = DataVault().input(prod, part, inputs=histnames)
        return data.read_multiple(n_hisits)
    low, high = multiple("low"), multiple("high")
    return [(l, h) for l, h in zip(low, high)]


@pytest.fixture
def real_data():
    return DataVault().input("data")


@pytest.fixture
def data():
    return (real_data, mc_data)


@pytest.mark.onlylocal
@pytest.mark.interactive
def test_scan_parameters(data, nbins=9):
    options = CompositeNonlinearityScanOptions(
        particle="#pi^{0}",
        nbins=nbins
    )
    options.factor = 1.

    with open_loggs("searching the optimal parameters") as loggs:
        chi2ndf = NonlinearityScan(options, chi2_=chi2).transform(data, loggs)
        su.write(chi2ndf, "search_nonlinearity_scan.root")
        Comparator().compare(chi2ndf)
