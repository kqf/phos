import pytest

import spectrum.broot as br
import spectrum.plotter as plt
from spectrum.spectra import spectrum
from spectrum.output import open_loggs
from spectrum.pipeline import ParallelPipeline
from spectrum.pipeline import SingleHistReader
from spectrum.vault import DataVault


@pytest.fixture
def data():
    data = (
        DataVault().input("theory", "incnlo high", histname="#sigma_{total}"),
        DataVault().input("theory", "incnlo low", histname="#sigma_{total}"),
    )
    with open_loggs() as loggs:
        predictions = ParallelPipeline([
            ("mu1", SingleHistReader()),
            ("mu2", SingleHistReader()),
        ]).transform(data, loggs=loggs)
    return predictions


@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
])
def test_pion_spectrum(data, tcm, oname):
    pion = spectrum("#pi^{0}")
    pion.Fit(tcm, "R")
    pion.SetTitle("Data")
    histograms = [pion] + list(data)
    ratios = [br.ratio(h, tcm) for h in histograms]
    confidence = br.shaded_region("pQCD", *ratios[1:])
    confidence.SetTitle("NLO, PDF: CTEQ5")
    plt.plot(
        [ratios[0], confidence],
        ytitle="#frac{Data, NLO}{TCM fit}",
        xtitle="#it{p}_{T} (GeV/#it{c})",
        logy=False,
        ylimits=(0, 10.),
        csize=plt.wide_csize,
        tmargin=0.01,
        rmargin=0.01,
        lmargin=0.1,
        yoffset=1.,
        options=["p", "f"],
        oname=oname.format("/pQCD/")
    )
