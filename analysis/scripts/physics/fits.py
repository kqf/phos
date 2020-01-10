import pytest  # noqa

import spectrum.broot as br
from spectrum.spectra import spectrum
from spectrum.plotter import plot
from spectrum.constants import invariant_cross_section_code


@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    "#eta",
])
def test_tsallis_tcm_fit(particle, tcm, tsallis, oname):
    cs = spectrum(particle)
    cs.SetTitle("Data")
    cs.Fit(tcm, "RQ")
    cs.Fit(tsallis, "RQ")
    br.report(tcm, particle)
    br.report(tsallis, particle)
    plot(
        [cs, tcm, tsallis],
        ytitle=invariant_cross_section_code(),
        xtitle="p_{T} (GeV/#it{c})",
        # xlimits=(0.7, 22),
        csize=(96, 128),
        ltitle="{} #rightarrow #gamma#gamma".format(particle),
        legend_pos=(0.65, 0.7, 0.8, 0.88),
        yoffset=1.4,
        more_logs=False,
        oname=oname.format("phenomenology/fits_"),
    )
