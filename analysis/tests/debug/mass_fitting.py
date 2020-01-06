from __future__ import print_function
import pytest
import ROOT

from spectrum.comparator import Comparator
import spectrum.broot as br


@pytest.fixture
def mass(filename="mass.root"):
    infile = ROOT.TFile(filename)
    histogram = infile.Get("mass_data_copied")
    return histogram


@pytest.fixture
def width(filename="width.root"):
    infile = ROOT.TFile(filename)
    histogram = infile.Get("width_data_copied")
    return histogram


@pytest.mark.skip('')
@pytest.mark.interactive
@pytest.mark.onlylocal
def test_masss_fitting(mass):
    fitf = ROOT.TF1("mass",
                    "TMath::Exp([0] * x) * [1] + [2]", 0, 20)
    fitf.SetParameters(*[-0.38271249157687853,
                         0.0014294353484205393,
                         0.13681699068487807])
    mass.Fit(fitf, "R")
    print("Mass parameters", br.pars(fitf))
    Comparator().compare(mass)


@pytest.mark.interactive
@pytest.mark.onlylocal
def test_width_fitting(width):
    fitf = ROOT.TF1("width",
                    "sqrt([0] ** 2 + ([1] / x) ** 2 + ([2] * x) ** 2)", 2, 20)
    fitf.SetParameters(*[0.004073830333585946,
                         0.008147508911668301,
                         0.00019036093293625441])
    width.Fit(fitf, "R")
    print("Width chi^2/ndf", fitf.GetChisquare() / fitf.GetNDF())
    print("Width parameters", br.pars(fitf))
    Comparator().compare(width)
