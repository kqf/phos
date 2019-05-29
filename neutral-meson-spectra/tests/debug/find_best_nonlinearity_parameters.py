import pytest
import ROOT
import spectrum.sutils as su
from spectrum.broot import BROOT as br
from spectrum.comparator import Comparator
from spectrum.options import CompositeNonlinearityScanOptions
from spectrum.output import AnalysisOutput
from tools.scan import NonlinearityScan, form_histnames
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


def test_scan_parameters(data, nbins=9):
    prod = "single #pi^{0} nonlinearity scan"
    histnames = form_histnames(nbins)
    low = DataVault().input(prod, "low", inputs=histnames)
    high = DataVault().input(prod, "high", inputs=histnames)

    options = CompositeNonlinearityScanOptions(
        particle="#pi^{0}",
        nbins=nbins
    )
    options.factor = 1.

    low, high = low.read_multiple(2), high.read_multiple(2)
    mc_data = [(l, h) for l, h in zip(low, high)]

    chi2ndf = NonlinearityScan(options, chi2_=chi2).transform(
        [DataVault().input("data"), mc_data],
        loggs=AnalysisOutput("searching the optimal parameters")
    )
    # TODO: Add this to the output
    su.write(chi2ndf, "search_nonlinearity_scan.root")
    Comparator().compare(chi2ndf)
