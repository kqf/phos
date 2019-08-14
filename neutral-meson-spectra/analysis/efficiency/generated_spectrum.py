from __future__ import print_function
import pytest
import ROOT

from spectrum.comparator import Comparator
from spectrum.input import SingleHistInput
from vault.datavault import DataVault


def fit_function(particle):
    tsallis = ROOT.TF1(
        "f", "x[0] * (x[0])*[0]/2./3.1415*([2]-1.)*([2]-2.)/([2]*[1]*([2]*[1]+[4]*([2]-2.))) * (1.+(sqrt((x[0])*(x[0])+[3]*[3])-[4])/([2]*[1])) ** (-[2])", 0, 20)  # noqa
    tsallis.SetParameters(21.339890553914014,
                          0.08359755308503322, 7.334946541612603)
    tsallis.FixParameter(3, 0.135)
    tsallis.FixParameter(4, 0.135)
    tsallis.SetLineColor(46)
    return tsallis


@pytest.fixture
def data():
    return (
        DataVault().input("single #pi^{0}", "low", "PhysEff"),
        DataVault().input("single #pi^{0}", "high", "PhysEff")
    )


@pytest.fixture
def target_hist():
    return "hPt_#pi^{0}_primary_standard"


def test_generated_distribution(target_hist, data):
    for prod in data:
        generated = SingleHistInput(target_hist).transform(prod)
        generated.Scale(1. / generated.Integral())
        function = fit_function("#pi^{0}")
        Comparator().compare(generated, function.GetHistogram())
