import pytest
import json
import six

import spectrum.broot as br
import spectrum.plotter as plt
from spectrum.pipeline import ParallelPipeline, FunctionTransformer
from spectrum.pipeline import TransformerBase, Pipeline
from spectrum.output import open_loggs
from spectrum.vault import FVault


class SpectrumFitter(TransformerBase):
    def __init__(self, parameters):
        self.parameters = parameters

    def transform(self, hist, loggs):
        fitf = FVault().tf1("tsallis")
        for i, p in enumerate(self.parameters):
            fitf.FixParameter(i, p)
        hist.Fit(fitf)
        plt.plot([hist, fitf])
        return hist


def hepdata(parameters):
    return Pipeline([
        ("raw", FunctionTransformer(br.from_hepdata, True)),
        ("fit", SpectrumFitter(parameters))
    ])


@pytest.fixture
def data():
    with open("config/predictions/hepdata.json") as f:
        data = json.load(f)["#pi^{0}"]
    return data


@pytest.fixture
def tsallis_pars():
    with open("config/predictions/tsallis.json") as f:
        data = json.load(f)["#pi^{0}"]
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
            out = ParallelPipeline(steps).transform([link], loggs)
            plt.plot(out)
