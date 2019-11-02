import ROOT
import pytest  # noqa

import spectrum.sutils as su
from spectrum.spectra import spectrum
from spectrum.plotter import plot
from spectrum.constants import invariant_cross_section_code


def report(func, particle):
    particle = su.spell(particle)
    pattern = r"\def \{particle}{func}{par}{err} {{{val:.3g}}}"
    for i in range(func.GetNpar()):
        print(pattern.format(
            particle=particle,
            func=func.GetName(),
            par=func.GetParName(i),
            val=func.GetParameter(i),
            err=""
        ))
        print(pattern.format(
            particle=particle,
            func=func.GetName(),
            par=func.GetParName(i),
            val=func.GetParError(i),
            err="Error"
        ))

    print(r"\def \{particle}{func}Chi {{{val:.3g}}}".format(
        particle=particle,
        func=func.GetName(),
        val=func.GetChisquare() / func.GetNDF()
    ))
    xmin, xmax = ROOT.Double(0), ROOT.Double(0)
    func.GetRange(xmin, xmax)

    print(r"\def \{particle}{func}MinPt {{{val:.3g}}}".format(
        particle=particle,
        func=func.GetName(),
        val=xmin
    ))

    print(r"\def \{particle}{func}MaxPt {{{val:.3g}}}".format(
        particle=particle,
        func=func.GetName(),
        val=xmax
    ))


@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    "#eta",
])
def test_tcm_fit(particle, tcm, tsallis, oname):
    cs = spectrum(particle)
    cs.SetTitle("Data")
    cs.Fit(tcm, "RQ")
    cs.Fit(tsallis, "RQ")
    print()
    report(tcm, particle)
    report(tsallis, particle)
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
        oname=oname.format("phenomenology/fits/"),
    )
