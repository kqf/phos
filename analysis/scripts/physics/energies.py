import pytest
import json
import six

import spectrum.broot as br
from spectrum.pipeline import FunctionTransformer
from spectrum.pipeline import ParallelPipeline
from spectrum.output import open_loggs
from spectrum.spectra import spectrum
from spectrum.plotter import plot
from spectrum.constants import invariant_cross_section_code


@pytest.fixture
def data(particle):
    with open("config/predictions/hepdata.json") as f:
        data = json.load(f)[particle]
    labels, links = zip(*six.iteritems(data))
    steps = [(l, FunctionTransformer(br.from_hepdata, True)) for l in labels]
    with open_loggs() as loggs:
        histograms = ParallelPipeline(steps).transform(links, loggs)
    spectra = sorted(histograms, key=lambda x: x.energy)
    measured = spectrum(particle)
    measured.SetTitle("pp, #sqrt{#it{s}} = 13 TeV")
    spectra.append(measured)

    for i, cs in enumerate(spectra):
        cs.Scale(10 ** i)
        cs.SetTitle(cs.GetTitle() + " #times 10^{{{}}}".format(i))
    return spectra[::-1]


@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    "#eta",
])
def test_downloads_from_hepdata(particle, data, ltitle):
    plot(
        data,
        ytitle=invariant_cross_section_code(),
        xtitle="#it{p}_{T} (GeV/#it{c})",
        logx=False,
        ltitle=ltitle,
        legend_pos=(0.6, 0.7, 0.7, 0.88),
        oname="results/discussion/energies/{}.pdf".format(br.spell(particle))
    )
