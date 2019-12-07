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


@pytest.mark.parametrize("colors", [
    "coolwarm",
    "levels",
    "auto"
])
@pytest.mark.parametrize("options", ["p", ["E5", "E5", "E5"]])
def test_plots_histograms(data, colors, options, stop):
    plot(data, colors=colors, options=options, stop=stop)


@pytest.mark.skip
@pytest.mark.parametrize("colors", [
    "coolwarm",
    "levels",
    "auto"
])
def test_plots_functions(data, functions, colors, stop):
    plot(data + functions, colors=colors, stop=stop)


@pytest.mark.skip
@pytest.mark.parametrize("colors", [
    "coolwarm",
    "levels",
    "auto"
])
def test_hplots_histograms(data, colors, stop):
    hplot(data, colors=colors, stop=stop)
