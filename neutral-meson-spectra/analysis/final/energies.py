import pytest
import json
import six

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
        hist.Scale(item["scale"])
        hist.energy = item["energy"]
        return hist


class ErrorsTransformer(TransformerBase):
    def transform(self, data, loggs):
        for i in br.range(data):
            data.SetBinError(i, 0.000001)
        # print(br.edges(data))
        return data


def hepdata():
    return Pipeline([
        ("raw", HepdataInput()),
        ("errors", ErrorsTransformer()),
    ])


@pytest.fixture
def data():
    with open("config/predictions/hepdata-pion.json") as f:
        data = json.load(f)
    return data


@pytest.mark.onlylocal
@pytest.mark.interactive
def test_downloads_from_hepdata(data):
    labels, links = zip(*six.iteritems(data))
    steps = [(l, hepdata()) for l in labels]
    pion = spectrum("#pi^{0}")
    pion.Scale(57.8 * 1e3)
    steps.append(("13 TeV", FunctionTransformer(lambda x, loggs: pion)))
    links = list(links)
    links.append(None)
    with open_loggs() as loggs:
        ComparePipeline(steps, plot=True).transform(links, loggs)
