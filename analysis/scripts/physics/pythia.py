import pytest

import spectrum.plotter as plt
from spectrum.spectra import spectrum
from spectrum.constants import invariant_cross_section_code


@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    "#eta"
])
def test_compare_with_pythia(pythia6, particle, tcm, oname):
    cs = spectrum(particle)
    cs.SetTitle("Data")
    cs.Fit(tcm, "RQ")
    plt.plot(
        [cs, pythia6, tcm],
        ytitle=invariant_cross_section_code(),
        xtitle="#it{p}_{T} (GeV/#it{c})",
        xlimits=(2, 22),
        ylimits=(0.0002, 400),
        ltitle="{} #rightarrow #gamma#gamma".format(particle),
        legend_pos=(0.65, 0.7, 0.8, 0.88),
        # yoffset=1.4,
        more_logs=False,
        oname=oname.format("pythia/"),
    )
