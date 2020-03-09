import ROOT
import pytest

import spectrum.comparator as cmpr


@pytest.mark.fixture
def fit_function():
    func_nonlin = ROOT.TF1("func_nonlin", "pol2(0) + pol1(3)", 0, 100)
    func_nonlin.SetParLimits(0, -10, 0)
    func_nonlin.SetParameter(0, -1.84679e-02)
    func_nonlin.SetParameter(1, -4.70911e-01)
    func_nonlin.SetParameter(2, -4.70911e-01)

    func_nonlin.SetParameter(3, 0.35)
    func_nonlin.SetParameter(4, 0.78)
    return func_nonlin


def test_compares_two_hists(data, stop):
    diff = cmpr.Comparator(stop=stop)
    data[2].SetTitle("Comparing double plots")
    diff.compare(data[2], data[1])


def test_compares_ratios(data, stop):
    diff = cmpr.Comparator(stop=stop)
    main = data[1]
    main.SetTitle("Testing yaxis maximal range for off scale points")
    distorted = main.Clone(main.GetName() + "_clone")
    distorted.SetBinContent(80, distorted.GetBinContent(80) * 100)
    distorted.label = "distorted"
    diff.compare(main, distorted)


def test_compares_two_fitted_hists(data, stop):
    title = "Comparing different ratiofit ranges {!r}"
    ranges = (0, 0), (0, 10), (10, 5), (4, 8)

    for frange in ranges:
        data[2].SetTitle(title.format(frange))
        data[2].fitfunc = ROOT.TF1("f1", "pol1(0)", *frange)
        diff = cmpr.Comparator(stop=stop)
        diff.compare(data[2], data[1])


def test_compare_nonlinear_plots(data, fit_function, stop):
    diff = cmpr.Comparator(stop=stop)
    # diff.compare(data[2], data[1])
    data[0].SetTitle("Comparing nonlinear fit function")
    data[0].fitfunc = fit_function()
    diff.compare(data[0], data[1])


def test_rebinned_plots(data, stop):
    diff = cmpr.Comparator(stop=stop)
    # diff.compare(data[2], data[1])

    data[0].SetTitle("Test Rebin Function second")
    data[0].Rebin(2)
    diff.compare(data[0], data[1])

    data[0].SetTitle("Test Rebin Function first")
    data[1].Rebin(2)
    diff.compare(data[0], data[1])


def test_ignores_ratio_plot(data, stop):
    diff = cmpr.Comparator(stop=stop)

    data[0].SetTitle("Test ignore ratio plot: This should be OK")
    diff.compare(data[0], data[1])

    diff = cmpr.Comparator(rrange=(-1, -1), stop=stop)

    data[0].SetTitle(
        "Test ignore ratio plot: This plot should be without ratio pad")
    diff.compare(data[0], data[1])
