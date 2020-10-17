import pytest

import spectrum.broot as br
import spectrum.plotter as plt

from spectrum.pipeline import TransformerBase, Pipeline, DataFitter
from spectrum.spectra import energies, DataEnergiesExtractor
from spectrum.constants import invariant_cross_section_code


def u_(pt, energy, lambda_=0.27, Q0=1, W0=1e-3):
    W = W0 * energy
    return (pt ** 2) / Q0 * (pt / W) ** lambda_


# Empirical approximation of <pT(s)>
def average_pt(energy, a=0.235, n=0.096):
    return a * energy ** n


class UTransformer(TransformerBase):
    def transform(self, x, loggs):
        edges = br.edges(x.tot)
        u_edges = u_(edges, x.energy)

        u = br.PhysicsHistogram(
            self._transform(x.tot, u_edges),
            self._transform(x.stat, u_edges),
            self._transform(x.syst, u_edges),
            energy=x.energy,
        )
        u.fitf = x.fitf
        return u

    @staticmethod
    def _transform(hist, edges):
        return br.table2hist(
            "{}_u".format(hist.GetName()),
            hist.GetTitle(),
            br.bins(hist).contents,
            br.bins(hist).errors,
            edges
        )


def u_spectra(fitf):
    return Pipeline([
        ("cyield", DataEnergiesExtractor()),
        ("fit", DataFitter(fitf)),
        ("u", UTransformer()),
    ])


@pytest.fixture
def u_data(particle, tcm):
    spectra = sorted(
        energies(particle, u_spectra(tcm)),
        key=lambda x: -x.energy
    )
    return spectra


@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    "#eta",
], scope="module")
def test_scaled_spectra(u_data, ltitle, oname):
    plt.plot(
        u_data,
        ytitle=invariant_cross_section_code(),
        xtitle="#it{u/u_{0}}",
        ltitle=ltitle,
        more_logs=False,
        legend_pos=(0.24, 0.15, 0.5, 0.35),
        oname=oname.format("u_scaling/u_normalized_cross_section_"),
    )
