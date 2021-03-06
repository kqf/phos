from __future__ import print_function
import pytest
import ROOT

from spectrum.comparator import Comparator
from spectrum.pipeline import SingleHistReader
from spectrum.vault import DataVault


@pytest.fixture
def fitf(particle):
    tsallis = ROOT.TF1(
        "f", "x[0] * (x[0])*[0]/2./3.1415*([2]-1.)*([2]-2.)/([2]*[1]*([2]*[1]+[4]*([2]-2.))) * (1.+(sqrt((x[0])*(x[0])+[3]*[3])-[4])/([2]*[1])) ** (-[2])", 0, 20)  # noqa
    tsallis.SetParameters(21.339890553914014,
                          0.08359755308503322, 7.334946541612603)
    tsallis.FixParameter(3, 0.135)
    tsallis.FixParameter(4, 0.135)
    tsallis.SetLineColor(46)
    return tsallis


@pytest.fixture
def spmc(particle):
    production = "single {}".format(particle)
    hname = "hPt_{}_primary_standard".format(particle)
    return (
        DataVault().input(production, "low", "PhysEff", histname=hname),
        DataVault().input(production, "high", "PhysEff", histname=hname),
    )


@pytest.mark.parametrize("particle", [
    "#pi^{0}",
])
def test_generated_distribution(particle, fitf, spmc, stop):
    for prod in spmc:
        generated = SingleHistReader().transform(prod)
        generated.logy = True
        generated.Scale(1. / generated.Integral())
        Comparator(stop=stop).compare(generated, fitf.GetHistogram())
