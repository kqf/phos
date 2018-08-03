import unittest
import ROOT

from spectrum.comparator import Comparator
from spectrum.broot import BROOT as br


class TestFitting(unittest.TestCase):

    @unittest.skip('')
    def test_masss_fitting(self):
        filename = "mass.root"
        infile = ROOT.TFile(filename)
        fitf = ROOT.TF1("mass",
                        "TMath::Exp([0] * x) * [1] + [2]", 0, 20)
        fitf.SetParameters(*[-0.38271249157687853, 0.0014294353484205393, 0.13681699068487807])
        histogram = infile.Get("mass_data_copied")
        histogram.Fit(fitf, "R")
        print br.pars(fitf)
        Comparator().compare(histogram)

    def test_width_fitting(self):
        filename = "width.root"
        infile = ROOT.TFile(filename)
        fitf = ROOT.TF1("width",
                        "sqrt([0] ** 2 + ([1] / x) ** 2 + ([2] * x) ** 2)", 2, 20)
        fitf.SetParameters(*[0.004073830333585946, 0.008147508911668301, 0.00019036093293625441])
        histogram = infile.Get("width_data_copied")
        histogram.Fit(fitf, "R")
        print fitf.GetChisquare() / fitf.GetNDF()
        print br.pars(fitf)
        Comparator().compare(histogram)
