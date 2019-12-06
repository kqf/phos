import pytest

from spectrum.plotter import plot, hplot
from vault.formulas import FVault


@pytest.fixture
def functions(data):
    funcs = []
    for spectrum in data:
        func = FVault().tf1("tsallis")
        func.SetTitle("Tsallis fit")
        func.SetRange(0.3, 15)
        spectrum.Fit(func, "RQ0")
        funcs.append(func)
    return funcs


@pytest.fixture
def stop():
    return True


def test_plots_histograms(data, stop):
    plot(data, "p_{T}", "y", logy=True, logx=True, stop=stop)


def test_plots_functions(data, functions, stop):
    plot(data + functions, "p_{T}", "y", logy=True, logx=True, stop=stop)


def test_hplots_histograms(data, stop):
    hplot(data, "p_{T}", "y", logy=True, logx=True, stop=stop)
