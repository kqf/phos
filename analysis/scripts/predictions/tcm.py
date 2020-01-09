import ROOT
import pytest
import json
import numpy as np

import spectrum.broot as br
import spectrum.constants as ct
from spectrum.pipeline import TransformerBase, Pipeline
from spectrum.vault import FVault
from spectrum.plotter import plot


class HepdataInput(TransformerBase):
    def __init__(self, table_name="Table 1", histname="Hist1D_y1", plot=False):
        super(HepdataInput, self).__init__(plot)
        self.histname = histname

    def transform(self, item, loggs):
        filename = ".hepdata-cachedir/{}".format(item["file"])
        br.io.hepdata(item["hepdata"], filename, item["table"])
        hist = br.io.read(filename, item["table"], self.histname)
        hist.logy = True
        hist.logx = True
        hist.Scale(item["scale"])
        hist.energy = item["energy"]
        # fitf = ROOT.TF1("tsallis", tsallis, 0, 100, 4)
        fitf = ROOT.TF1("tsallis", FVault().func("tsallis"), 0, 100, 4)
        fitf = FVault().tf1("tsallis")
        fitf.FixParameter(0, 2.4 * 100000)
        fitf.FixParameter(1, 0.139)
        fitf.FixParameter(2, 6.88)
        fitf.FixParameter(3, 0.134976)
        fitf.FixParameter(4, 0.134976)
        hist.Fit(fitf)
        return hist


def scale_bin_width(hist, rebins=None):
    hist = hist.Clone()
    width = 1
    for i in br.hrange(hist):
        if rebins is not None:
            width = rebins[i - 1] + 1
        hist.SetBinContent(i, hist.GetBinContent(i) / width)
    return hist


def meregd_bins(new, old):
    new, old = br.edges(new), br.edges(old)

    def nbins(a, b):
        return [pT for pT in old if a < pT < b]

    rebins = [len(nbins(*edge)) for edge in zip(new[:-1], new[1:])]
    return rebins


class SpectrumFitter(TransformerBase):
    def __init__(self, parameters):
        self.parameters = parameters

    def transform(self, hist, loggs):
        fitf = FVault().tf1("tsallis")
        for i, p in enumerate(self.parameters):
            fitf.FixParameter(i, p)
        hist.Fit(fitf)
        return hist


class ErrorsTransformer(TransformerBase):
    def transform(self, data, loggs):
        for i in br.hrange(data):
            data.SetBinError(i, 0.000001)
        # print(br.edges(data))
        return data


def hepdata(parameters):
    return Pipeline([
        ("raw", HepdataInput()),
        ("errors", ErrorsTransformer()),
        ("fit", SpectrumFitter(parameters))
    ])


@pytest.fixture
def data(system):
    with open("config/predictions/hepdata-pion.json") as f:
        data = json.load(f)
    return data[system]


@pytest.fixture
def tcm(data, eta=0.12, particle="#pi^{0}"):
    energy = data["energy"]
    mass = ct.mass(particle)
    doublemass = 2 * ct.mass(particle)
    func = FVault().tf1("tcm")
    eta_prime = eta - np.log(energy / doublemass)
    eta_prime_prime = eta + np.log(energy / doublemass)
    Te = 409 * np.exp(0.06 * eta_prime_prime) * doublemass ** 0.6
    T = 98 * np.exp(0.06 * eta_prime_prime) * doublemass ** 0.6
    n = 5.04 + 0.27 * eta_prime

    Aexp = 0.76 * (energy ** 2) ** 0.106
    etaexp = 0.692 + 0.293 * np.log(energy)
    sigmaexp = 0.896 + 0.136 * np.log(energy)
    expo = Aexp * (
        np.exp(- (eta - etaexp) ** 2 / 2 / sigmaexp ** 2) +
        np.exp(- (eta + etaexp) ** 2 / 2 / sigmaexp ** 2)
    )
    Apow = 0.13 * (energy ** 2) ** 0.175
    sigmapower = 0.217 + 0.235 * np.log(energy)
    power = Apow * np.exp(- eta ** 2 / 2 / sigmapower)
    Ae = 1. / 2 / Te / (mass + Te) * expo
    A = (n - 1) / n / T ** 2 * power
    func.SetParameter("n", n)
    func.SetParameter("T", T)
    func.SetParameter("Te", Te)
    func.SetParameter("Ae", Ae)
    func.SetParameter("A", A)
    func.SetParameter("M", mass)
    return func


@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("system", [
    "pp 7 TeV",
    "pp 0.9 TeV",
    "pp 2.76 TeV",
    "pp 8 TeV"
])
def test_downloads_from_hepdata(data, tcm):
    plot([tcm], logy=False, logx=False)
