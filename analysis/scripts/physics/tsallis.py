import pytest  # noqa

import spectrum.broot as br
from spectrum.spectra import spectrum
from spectrum.plotter import plot
from spectrum.constants import invariant_cross_section_code


@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("particle, ranges", [
    ("#pi^{0}", [0.8, 20]),
    ("#eta", [2.0, 20]),
])
def test_tsallis_tcm_fit(particle, ranges, tsallis, ltitle, stop, oname):
    cs = spectrum(particle)
    tsallis.SetRange(*ranges)
    cs.Fit(tsallis, "Q")
    br.report(tsallis, particle)
    plot(
        [cs, tsallis],
        ytitle=invariant_cross_section_code(),
        xtitle="p_{T} (GeV/#it{c})",
        # xlimits=(0.7, 22),
        csize=(96, 128),
        ltitle=ltitle,
        legend_pos=(0.65, 0.7, 0.8, 0.88),
        yoffset=1.4,
        more_logs=False,
        oname=oname.format("phenomenology/fits_"),
    )
    ratio = cs.Clone()
    ratio.Divide(tsallis)
    plot(
        [ratio],
        stop=stop,
        logy=False,
        ytitle=invariant_cross_section_code(),
        xtitle="p_{T} (GeV/#it{c})",
        # xlimits=(0.7, 22),
        csize=(96, 128),
        ltitle=ltitle,
        legend_pos=(0.65, 0.7, 0.8, 0.88),
        yoffset=1.4,
        more_logs=False,
        oname=oname.format("phenomenology/fits_"),
    )
