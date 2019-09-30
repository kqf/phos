import pytest
import json
import six

import spectrum.sutils as su
from spectrum.broot import BROOT as br
from spectrum.pipeline import TransformerBase, Pipeline, FunctionTransformer
from spectrum.pipeline import ComparePipeline
from spectrum.output import open_loggs
from spectrum.spectra import spectrum


class HepdataInput(TransformerBase):
    def __init__(self, table_name="Table 1", histname="Hist1D_y1", plot=False):
        super(HepdataInput, self).__init__(plot)
        self.histname = histname

    def transform(self, item, loggs):
        filename = ".hepdata-cachedir/{}".format(item["file"])
        br.io.hepdata(item["hepdata"], filename, item["table"])
        hist = br.io.read(filename, item["table"], self.histname)
        hist.logy = True
        hist.logx = False
        hist.GetXaxis().SetTitle("p_{T}, GeV/c")
        ytitle = "#frac{{1}}{{N_{{events}}}} #frac{{dN}}{{d p_{{T}}}}".format()
        hist.GetYaxis().SetTitle(ytitle)
        hist.SetTitle("")
        hist.Scale(item["scale"])
        hist.energy = item["energy"]
        return hist


class ErrorsTransformer(TransformerBase):
    def transform(self, data, loggs):
        for i in br.range(data):
            data.SetBinError(i, 1e-29)
        # print(br.edges(data))
        return data


def hepdata():
    return Pipeline([
        ("raw", HepdataInput()),
        ("errors", ErrorsTransformer()),
    ])


@pytest.fixture
def data(particle):
    filename = "config/predictions/hepdata-{}.json".format(su.spell(particle))
    with open(filename) as f:
        data = json.load(f)
    return data


@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    "#eta",
])
def test_downloads_from_hepdata(particle, data):
    labels, links = zip(*six.iteritems(data))
    steps = [(l, hepdata()) for l in labels]
    pion = spectrum(particle)
    steps.append(("pp 13 TeV", FunctionTransformer(lambda x, loggs: pion)))
    links = list(links)
    links.append(None)
    with open_loggs() as loggs:
        ComparePipeline(steps, plot=True).transform(links, loggs)
