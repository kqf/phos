import pytest
import json
import six

import spectrum.broot as br
from spectrum.pipeline import TransformerBase, Pipeline
from spectrum.pipeline import ParallelPipeline
from spectrum.comparator import Comparator
from spectrum.output import open_loggs
from spectrum.vault import FVault


class HepdataInput(TransformerBase):
    def __init__(self, table_name="Table 1", histname="Hist1D_y1", plot=False):
        super(HepdataInput, self).__init__(plot)
        self.histname = histname

    def transform(self, item, loggs):
        filename = ".hepdata-cachedir/{}".format(item["file"])
        br.io.hepdata(item["hepdata"], filename, item["table"])
        hist = br.io.read(filename, item["table"], self.histname)
        hist.logx = True
        hist.logy = True
        hist.label = item["title"]
        hist.Scale(item["scale"])
        hist.energy = item["energy"]
        hist.title = item["title"]
        return hist


class DataFitter(TransformerBase):
    def __init__(self):
        with open("config/predictions/tsallis-pion.json") as f:
            self.data = json.load(f)

    def transform(self, x, loggs):
        tsallis = FVault().tf1("tsallis", x.title.replace("pp", "#pi^{0}"))
        x.fitfunc = tsallis
        return x


def xt(edges=None):
    return Pipeline([
        ("cyield", HepdataInput()),
        ("fit", DataFitter()),
    ])


@pytest.fixture(scope="module")
def data():
    with open("config/predictions/hepdata-pion.json") as f:
        data = json.load(f)
    labels, links = zip(*six.iteritems(data))
    steps = [(l, xt()) for l in labels]
    with open_loggs() as loggs:
        histograms = ParallelPipeline(steps).transform(links, loggs)
    return [h for h in histograms if int(h.energy) == 900][0]


# Exact match: 8 TeV
# Slight deviation: 7 TeV
# Minor deviation: 2.76 TeV
# Exact match: 900 GeV

@pytest.mark.onlylocal
@pytest.mark.interactive
def test_xt_distribution(data):
    with br.tfile("CrossSectionALICE_05_10_17.root") as rfile:
        graph = rfile.Get("graphInvCrossSectionPi00900GeVCombA")
        hist = br.graph2hist(graph, data.Clone())
        hist.Scale(1e-6)
        hist.label = "pooja"
    Comparator().compare(hist, data)
