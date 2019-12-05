from spectrum.plotter import plot, hplot
from vault.formulas import FVault


def test_plots_histograms(data, stop):
    plot(data, "p_{T}", "y", logy=True, logx=True, stop=stop)


def test_plots_functions(data, stop):
    fitf = FVault().tf1("tsallis")
    fitf.SetTitle("approximation")
    data.append(fitf)
    plot(data, "p_{T}", "y", logy=True, logx=True, stop=stop)


def test_hplots_histograms(data, stop=True):
    hplot(data, "p_{T}", "y", logy=True, logx=True, stop=stop)
