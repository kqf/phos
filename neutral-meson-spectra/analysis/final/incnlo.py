import pytest

from spectrum.spectra import spectrum
from spectrum.output import open_loggs
from spectrum.pipeline import ParallelPipeline
from spectrum.input import SingleHistInput
from spectrum.plotter import plot
import spectrum.broot as br
from vault.datavault import DataVault
from vault.formulas import FVault


@pytest.fixture
def data():
    data = (
        DataVault().input("theory", "incnlo"),
        DataVault().input("theory", "7 TeV")
    )
    with open_loggs() as loggs:
        predictions = ParallelPipeline([
            ("mu1", SingleHistInput("#sigma_{total}")),
            ("mu2", SingleHistInput("#sigma_{total}")),
        ]).transform(data, loggs=loggs)
    return predictions


@pytest.mark.onlylocal
@pytest.mark.interactive
def test_pion_spectrum(data):
    pion = spectrum("#pi^{0}")
    pion.SetTitle("Data")
    histograms = [pion] + list(data)
    param = br.function2histogram(FVault().tf1("tcm", "#pi^{0} 13 TeV"), pion)
    ratios = [br.ratio(h, param) for h in histograms]
    confidence = br.shaded_region_hist("pQCD", *ratios[1:])
    confidence.SetTitle("pQCD NLO, 1/2 p_{T} < #mu < 2 p_{T}")
    plot(
        [ratios[0], confidence],
        ytitle="#frac{Data, NLO}{TCM fit}",
        xtitle="p_{T} (GeV/#it{c})",
        logy=False,
        logx=True,
        ylimits=(0, 10.),
        csize=(128, 96),
        legend_pos=(0.52, 0.72, 0.78, 0.88),
        yoffset=1.4,
        more_logs=True,
        oname="results/pQCD/pion.pdf"
    )
