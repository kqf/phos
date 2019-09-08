import pytest
import json
import six
from spectrum.broot import BROOT as br
from spectrum.pipeline import TransformerBase, Pipeline
from spectrum.pipeline import ComparePipeline
from spectrum.output import open_loggs
from spectrum.input import SingleHistInput

from vault.datavault import DataVault


class HepdataInput(TransformerBase):
    def __init__(self, table_name="Table 1", histname="Hist1D_y1", plot=False):
        super(HepdataInput, self).__init__(plot)
        self.table_name = table_name
        self.histname = histname

    def transform(self, item, loggs):
        print(item)
        filename = ".hepdata-cachedir/{}.root".format(item["hepdata"])
        # br.io.hepdata(item["hepdata"], filename)
        hist = br.io.read(filename, self.table_name, self.histname)
        hist.logy = True
        hist.logx = False
        hist.Scale(item["scale"])
        return hist


class ErrorsTransformer(TransformerBase):
    def transform(self, data, loggs):
        for i in br.range(data):
            data.SetBinError(i, 0.0001)
        data.Sumw2()
        return data


def theory_prediction(label):
    pipeline = Pipeline([
        ("raw", SingleHistInput("#sigma_{total}")),
        ("errors", ErrorsTransformer())
    ])
    return (label, pipeline)


@pytest.fixture
def datasets():
    with open("config/different-energies.json") as f:
        data = json.load(f)
    labels, links = zip(*six.iteritems(data))
    steps = [(l, HepdataInput()) for l in labels]
    steps.append(theory_prediction("INCNLO 13 TeV"))
    steps.append(theory_prediction("INCNLO 7 TeV"))

    links = list(links)
    links.append(DataVault().input("theory", "incnlo"))
    links.append(DataVault().input("theory", "7 TeV"))
    return steps, links


@pytest.mark.interactive
def test_downloads_from_hepdata(datasets):
    steps, links = datasets
    with open_loggs("compare yields") as loggs:
        ComparePipeline(steps, plot=True).transform(links, loggs)
