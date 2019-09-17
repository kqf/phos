import pytest
import numpy as np
import ROOT
# import spectrum.sutils as su
from vault.formulas import FVault


@pytest.fixture
def parameters():
    return [2.4 * 100000, 0.139, 6.88, 0.134976]


def tsallis(x, p):
    pt = x[0]
    # mass = p[0]
    norm, C, n, mass = p
    mt = ROOT.TMath.Sqrt(pt * pt + mass * mass)
    # n = p[1]
    # C = p[2]
    # norm = p[3]

    part1 = (n - 1.) * (n - 2)
    part2 = n * C * (n * C + mass * (n - 2.))
    part3 = part1 / part2
    part4 = 1. + (mt - mass) / n / C
    part5 = ROOT.TMath.Power(part4, -n)
    return norm * part3 * part5 / 2 / ROOT.TMath.Pi()


def test_tsallis(parameters):
    fitf = FVault().tf1("tsallis")
    fitf.SetParameters(*parameters)
    data = np.linspace(0, 20)
    np.testing.assert_almost_equal(
        [fitf.Eval(pt) for pt in data],
        [tsallis([pt], parameters) for pt in data]
    )
