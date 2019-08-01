import pytest
import json
import six
from spectrum.broot import BROOT as br
from spectrum.pipeline import TransformerBase
from spectrum.pipeline import ComparePipeline
from spectrum.output import open_loggs


class HepdataInput(TransformerBase):
    def __init__(self, table_name="Table 1", histname="Hist1D_y1", plot=False):
        super(HepdataInput, self).__init__(plot)
        self.table_name = table_name
        self.histname = histname

    def transform(self, link, loggs):
        filename = "{}.root".format(link)
        br.io.hepdata(link, filename)
        hist = br.io.read(filename, "Table 1", "Hist1D_y1")
        hist.logy = True
        hist.logx = False
        return hist


@pytest.fixture
def datasets():
    with open("config/different-energies.json") as f:
        data = json.load(f)
    labels, links = zip(*six.iteritems(data))
    steps = [(l, HepdataInput()) for l in labels]
    return steps, links


@pytest.mark.interactive
def test_downloads_from_hepdata(datasets):
    steps, links = datasets
    with open_loggs("compare yields") as loggs:
        ComparePipeline(steps, plot=True).transform(links, loggs)
