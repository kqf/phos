import pytest
import json
import six

from spectrum.spectra import DataExtractor
from spectrum.pipeline import ParallelPipeline, FunctionTransformer
from spectrum.pipeline import DataFitter, Pipeline
from spectrum.output import open_loggs
from spectrum.plotter import plot
from spectrum.constants import invariant_cross_section_code


def fitted(fitf):
    return Pipeline([
        ("cyield", DataExtractor()),
        ("fit", DataFitter(fitf)),
        ("show", FunctionTransformer(lambda x, **kwargs: plot([x, x.fitf]))),
    ])


@pytest.fixture
def data(particle, tcm):
    with open("config/predictions/hepdata.json") as f:
        data = json.load(f)[particle]
        data["pp 13 TeV"] = particle
    labels, links = zip(*six.iteritems(data))
    with open_loggs() as loggs:
        steps = [(l, fitted(tcm)) for l in labels]
        histograms = ParallelPipeline(steps).transform(links, loggs)
    spectra = sorted(histograms, key=lambda x: -x.energy)
    return spectra


@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    "#eta",
])
def test_downloads_from_hepdata(particle, stop, data, ltitle):
    plot(
        data,
        stop=stop,
        ytitle=invariant_cross_section_code(),
        xtitle="#it{p}_{T} (GeV/#it{c})",
        ltitle=ltitle,
        more_logs=True,
    )
