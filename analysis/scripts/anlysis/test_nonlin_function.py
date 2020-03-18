import ROOT
import pytest

import spectrum.broot as br
import spectrum.plotter as plt
from spectrum.vault import FVault


@pytest.fixture
def parameters():
    return {
        "old": [
            -0.014719244288611932,
            2 * 0.8017501954719543,
            1.050000000000015,
        ],
        "updated gamma": [
            -0.008502585550404397,
            1.063118454172695,
            1.0222154255076596
        ],
        "updated pi0": [
            -0.022361543707205396,
            1.9834455549215824,
            1.0160704760491277,
        ],
        "new pi0": [
            -0.023207895974126137,
            2.1705074159914495,
            1.0178019980200619
        ]
    }


@pytest.fixture
def functions(parameters):
    functions = [
        ROOT.TF1('f{}'.format(i), FVault().func("nonlinearity"), 0, 20)
        for i in parameters
    ]
    for i, (f, p) in enumerate(zip(functions, parameters)):
        f.SetTitle(p)
        f.SetParameters(*parameters[p])
        f.SetLineColor(br.auto_color_marker(i)[0])
    return functions


@pytest.mark.onlylocal
@pytest.mark.interactive
def test_nonlin_function(functions):
    plt.plot(functions, logx=False, logy=False, xtitle="#it{E}_{#gamma} (GeV)")
