import ROOT
import array
import pytest
import json
import six

from spectrum.broot import BROOT as br
from spectrum.pipeline import TransformerBase, Pipeline
from spectrum.pipeline import ComparePipeline
from spectrum.output import open_loggs
from vault.formulas import FVault


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
        # fitf = ROOT.TF1('tsallis', tsallis, 0, 100, 4)
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
    for i in br.range(hist):
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
        for i in br.range(data):
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
def data():
    with open("config/predictions/hepdata.json") as f:
        data = json.load(f)
    return data


@pytest.fixture
def tsallis_pars():
    with open("config/predictions/tsallis-pion.json") as f:
        data = json.load(f)

    pars = {
        label: [v["A"], v["C"], v["n"], v["M"]]
        for label, v in six.iteritems(data)
    }
    return pars


@pytest.mark.onlylocal
@pytest.mark.interactive
def test_downloads_from_hepdata(data, tsallis_pars):
    with open_loggs() as loggs:
        for label, link in six.iteritems(data):
            steps = [(label, hepdata(tsallis_pars[label]))]
            ComparePipeline(steps, plot=True).transform([link], loggs)
