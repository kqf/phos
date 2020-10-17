import pytest

import spectrum.broot as br
import spectrum.plotter as plt

from spectrum.pipeline import TransformerBase, Pipeline, DataFitter
from spectrum.spectra import energies, DataEnergiesExtractor
from spectrum.constants import invariant_cross_section_code


def tau(pt, energy, lambda_=0.27, Q0=1, W0=1e-3):
    W = W0 * energy
    return (pt ** 2) / Q0 * (pt / W) ** lambda_


# Empirical approximation of <pT(s)>
def average_pt(energy, a=0.235, n=0.096):
    return a * energy ** n


class UTransformer(TransformerBase):
    def __init__(self, lambda_, plot=False):
        super().__init__(plot)
        self.lambda_ = lambda_

    def transform(self, x, loggs):
        edges = br.edges(x.tot)
        tau_edges = tau(edges, x.energy, lambda_=self.lambda_)

        htau = br.PhysicsHistogram(
            self._transform(x.tot, tau_edges),
            self._transform(x.stat, tau_edges),
            self._transform(x.syst, tau_edges),
            energy=x.energy,
        )
        htau.fitf = x.fitf
        return htau

    @staticmethod
    def _transform(hist, edges):
        return br.table2hist(
            "{}_tau".format(hist.GetName()),
            hist.GetTitle(),
            br.bins(hist).contents,
            br.bins(hist).errors,
            edges
        )


def tau_spectra(fitf, lambda_):
    return Pipeline([
        ("cyield", DataEnergiesExtractor()),
        ("fit", DataFitter(fitf)),
        ("tau", UTransformer(lambda_=lambda_)),
    ])


@pytest.fixture
def tau_data(particle, lambda_, tcm):
    spectra = sorted(
        energies(particle, tau_spectra(tcm, lambda_)),
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
def test_scaled_spectra(tau_data, lambda_, ltitle, oname):
    plt.plot(
        tau_data,
        ytitle=invariant_cross_section_code(),
        xtitle="#tau (#lambda = {})".format(lambda_),
        ltitle=ltitle,
        more_logs=False,
        legend_pos=(0.24, 0.15, 0.5, 0.35),
        oname=oname.format("tau_scaling/tau_normalized_cross_section_"),
    )
