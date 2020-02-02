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
def test_tsallis_tcm_fit(particle, tcm, tsallis, ltitle, stop, oname):
    cs = spectrum(particle)
    cs.Fit(tcm, "RQ")
    cs.Fit(tsallis, "QR")
    br.report(tcm, particle, limits=True)
    br.report(tsallis, particle, limits=True)

    # Apply only after fitting. Extend the pT range for better visualisation
    if particle == "#pi^{0}":
        tsallis.SetRange(1.5, tcm.GetXmax())
    if particle == "#eta":
        tsallis.SetRange(tsallis.GetXmin(), tcm.GetXmax())

    plot(
        [cs, tcm, tsallis],
        stop=stop,
        ytitle=invariant_cross_section_code(),
        xtitle="#it{p}_{T} (GeV/#it{c})",
        # xlimits=(0.7, 22),
        csize=(96, 128),
        ltitle=ltitle,
        legend_pos=(0.65, 0.7, 0.8, 0.88),
        yoffset=1.4,
        more_logs=False,
        oname=oname.format("phenomenology/fits_"),
    )
