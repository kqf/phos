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


def test_generated_distribution():
    data = "low", "high"
    for prod in data:
        function = fit_function("#pi^{0}")
        generated = SingleHistInput(
            'hPt_#pi^{0}_primary_standard').transform(
            DataVault().input("single #pi^{0}", prod)
        )
        generated.Scale(1. / generated.Integral())
        diff = Comparator()
        diff.compare(generated, function)


def test_integral_over_tsallis_curve():
    tsallis = fit_function("#pi^{0}")
    print tsallis.Integral(0, 20)
