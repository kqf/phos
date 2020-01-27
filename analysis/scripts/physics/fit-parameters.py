import pytest
import json
import six

import spectrum.broot as br
from spectrum.pipeline import TransformerBase
from spectrum.pipeline import ParallelPipeline
from spectrum.output import open_loggs
from spectrum.spectra import spectrum
from spectrum.plotter import plot
from spectrum.constants import invariant_cross_section_code


class HepdataInput(TransformerBase):
    def __init__(self, table_name="Table 1",
                 histname="Graph1D_y1", plot=False):
        super(HepdataInput, self).__init__(plot)
        self.histname = histname

    def transform(self, item, loggs):
        filename = ".hepdata-cachedir/{}".format(item["file"])
        br.io.hepdata(item["hepdata"], filename, item["table"])
        graph = br.io.read(filename, item["table"], self.histname)
        hist = br.graph2hist(graph)
        hist.GetXaxis().SetTitle("#it{p}_{T} (GeV/#it{c})")
        hist.SetTitle(item["title"])
        hist.Scale(item["scale"])
        hist.energy = item["energy"]
        return hist


@pytest.fixture
def data(particle, tsallis, tcm, stop):
    with open("config/predictions/hepdata.json") as f:
        data = json.load(f)[particle]
    labels, links = zip(*six.iteritems(data))
    steps = [(l, HepdataInput()) for l in labels]
    with open_loggs() as loggs:
        histograms = ParallelPipeline(steps).transform(links, loggs)
    spectra = sorted(histograms, key=lambda x: x.energy)
    measured = spectrum(particle)
    measured.SetTitle("pp, #sqrt{#it{s}} = 13 TeV")
    measured.energy = 13
    spectra.append(measured)
    for data in spectra:
        tsallis.SetRange(0, 40)
        tcm.SetRange(0, 40)
        data.Fit(tsallis, "QR", "", 0, 40)
        data.Fit(tcm, "QR", "", 0, 40)
        plot([data, tsallis, tcm], stop=stop)
    return spectra


@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    "#eta",
])
def test_downloads_from_hepdata(particle, stop, data):
    plot(
        data,
        stop=stop,
        ytitle=invariant_cross_section_code(),
        xtitle="#it{p}_{T} (GeV/#it{c})",
        # xlimits=(0.7, 22),
        csize=(96, 128),
        ltitle="{} #rightarrow #gamma#gamma".format(particle),
        # legend_pos=(0.65, 0.7, 0.8, 0.88),
        legend_pos=(0.52, 0.72, 0.78, 0.88),
        yoffset=1.4,
        more_logs=True,
    )
