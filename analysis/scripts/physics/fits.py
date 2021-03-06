import pytest  # noqa

import spectrum.broot as br
import spectrum.plotter as plt
from spectrum.spectra import spectrum
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

    plt.plot(
        [cs, tcm, tsallis],
        stop=stop,
        ytitle=invariant_cross_section_code(),
        xtitle="#it{p}_{T} (GeV/#it{c})",
        ltitle=ltitle,
        oname=oname.format("phenomenology/fits_"),
    )
