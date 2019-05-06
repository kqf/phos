from __future__ import print_function

import ROOT
import pytest

from vault.formulas import FVault
from spectrum.comparator import Comparator


def parameters():
    return [
        0.014960701090585591,
        0.287830380417601,
        9.921003040859755
    ]


@pytest.mark.onlylocal
@pytest.mark.interactive
def test_parameters(parameters):
    fv = FVault()
    functions = [
        ROOT.TF1('f' + str(i), fv.func("tsallis"), 0, 20)
        for i in range(2)
    ]

    for change in [0, 1, 2]:
        ROOT.gStyle.SetPalette(51)
        for i, func in enumerate(functions):
            for ip, par in enumerate(parameters):
                parvalue = par + 0.01 * i * (change == ip)
                func.SetParameter(ip, parvalue)
                func.SetLineColor(i + 1)

            func.Draw("same" if i != 0 else "apl")

        Comparator().compare(
            map(lambda x: x.GetHistogram(), functions)
        )


def parameters_normalized():
    return [
        0.2622666593790998 / 0.0119143016137,
        0.08435275184952101,
        7.356520554717935,
        0.135,
        0.135
    ]


@pytest.mark.onlylocal
@pytest.mark.interactive
def test_integral(parameters_normalized):
    tsallis = ROOT.TF1('tsallis', FVault().func("tsallis"), 0, 20)
    tsallis.SetParameters(*parameters_normalized)
    print(tsallis.Integral(0, 20))
