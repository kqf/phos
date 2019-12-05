import pytest

from spectrum.plotter import plot, hplot
from vault.formulas import FVault


@pytest.fixture
def functions(data):
    funcs = []
    for d in data:
        func = FVault().tf1("tsallis")
        d.Fit(func)
        funcs.append(func)
    return funcs


def test_plots_histograms(data, stop):
    plot(data, "p_{T}", "y", logy=True, logx=True, stop=stop)


def test_plots_functions(data, functions, stop):
    plot(data + functions, "p_{T}", "y", logy=True, logx=True, stop=stop)


def test_hplots_histograms(data, stop):
    hplot(data, "p_{T}", "y", logy=True, logx=True, stop=stop)
