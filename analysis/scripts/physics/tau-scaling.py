import pytest

import spectrum.broot as br
import spectrum.plotter as plt

from spectrum.pipeline import TransformerBase, Pipeline, DataFitter
from spectrum.spectra import energies, DataEnergiesExtractor
from spectrum.constants import invariant_cross_section_code


class TauTransformer(TransformerBase):
    def transform(self, x, loggs):
        edges = br.edges(x.tot)
        xtedges = 2 * edges / x.energy

        xt = br.PhysicsHistogram(
            self._transform(x.tot, xtedges),
            self._transform(x.stat, xtedges),
            self._transform(x.syst, xtedges),
            energy=x.energy,
        )
        xt.fitf = x.fitf
        return xt

    @staticmethod
    def _transform(hist, edges):
        return br.table2hist(
            "{}_tau".format(hist.GetName()),
            hist.GetTitle(),
            br.bins(hist).contents,
            br.bins(hist).errors,
            edges
        )


def xt(fitf):
    return Pipeline([
        ("cyield", DataEnergiesExtractor()),
        ("fit", DataFitter(fitf)),
        ("xt", TauTransformer()),
    ])


@pytest.fixture
def tau_data(particle, tcm):
    spectra = sorted(
        energies(particle, xt(tcm)),
        key=lambda x: -x.energy
    )
    return spectra


@pytest.fixture
def combined_n(xtrange):
    return 5.099, 0.009


@pytest.fixture
def xtrange():
    return 2.9e-03, 1.05e-02


@pytest.fixture
def tau_sdata(tau_data, combined_n):
    scaled = []
    for h in tau_data:
        s = h.Clone("{}_scaled".format(h.GetName()))
        s.Scale(h.energy ** combined_n[0])
        scaled.append(s)
    return scaled


@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    "#eta",
], scope="module")
def test_scaled_spectra(tau_sdata, combined_n, ltitle, oname):
    title = "(#sqrt{{#it{{s}}}})^{{{n:.3f}}} (GeV)^{{{n:.3g}}} #times {t}"
    plt.plot(
        tau_sdata,
        ytitle=title.format(n=combined_n[0], t=invariant_cross_section_code()),
        xtitle="#it{x}_{T}",
        ltitle=ltitle,
        more_logs=False,
        legend_pos=(0.24, 0.15, 0.5, 0.35),
        oname=oname.format("xt_scaling/xt_normalized_cross_section_"),
    )
