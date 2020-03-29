from __future__ import print_function
import array
import os
import random
import json

import numpy as np
import pytest
import ROOT

import spectrum.broot as br
from spectrum.comparator import Comparator
from spectrum.options import Options
import spectrum.sutils as su


# NB: Don't use broot in write functions
#     as it's important to test without broot
#

@pytest.fixture
def edges():
    with open("config/pt.json") as f:
        data = json.load(f)["#pi^{0}"]
    return data["ptedges"]


@pytest.fixture
def write_histogram(wfilename, wselection, whistname):
    hist = ROOT.TH1F(whistname, 'reading from a rootfile', 10, -3, 3)
    hist.FillRandom('gaus')
    tlist = ROOT.TList()
    tlist.SetOwner(True)
    tlist.Add(hist)
    with br.tfile(wfilename, "recreate"):
        tlist.Write(wselection, ROOT.TObject.kSingleKey)
    yield br.clone(hist)
    os.remove(wfilename)


def write_histograms(filename, selection, histnames):
    hists = [ROOT.TH1F(histname, '', 10, -3, 3) for histname in histnames]

    tlist = ROOT.TList()
    tlist.SetOwner(True)
    for hist in hists:
        hist.FillRandom('gaus')
        tlist.Add(hist)

    with br.tfile(filename, "recreate"):
        tlist.Write(selection, ROOT.TObject.kSingleKey)
    return list(map(br.clone, hists))


@pytest.fixture
def written_histograms(wfilename, wselection, whistnames):
    yield write_histograms(wfilename, wselection, whistnames)
    os.remove(wfilename)


@pytest.fixture(scope="module")
def nominal_hist():
    nominal_hist = ROOT.TH1F("nominal_hist", "Testing", 100, -10, 10)
    nominal_hist.FillRandom("gaus")
    return nominal_hist


def test_draw(stop, nominal_hist):
    assert nominal_hist is not None
    with su.canvas(stop=stop):
        nominal_hist.Draw()


def test_clone(stop, nominal_hist):
    hist2 = br.clone(nominal_hist)
    assert nominal_hist.GetEntries() == hist2.GetEntries()


def test_copy(stop, nominal_hist):
    hist2 = br.copy(nominal_hist)
    assert not nominal_hist.GetEntries() == hist2.GetEntries()


def test_projection_saves_area(stop):
    # NB: Bin according to this sequence https://oeis.org/A000124
    #     so the bin width of a projection hist always increases
    #
    carter, ncarter = lambda n: int(n * (n + 1) / 2 + 1), 16

    nbinsx, startx, stopx = carter(ncarter), -10, 10
    nbinsy, starty, stopy = 100, -10, 10
    hist = ROOT.TH2F("test", "", nbinsx, startx, stopx, nbinsy, starty, stopy)

    # Fill random values
    for i in br.hrange(hist):
        for j in br.hrange(hist, 'y'):
            hist.SetBinContent(i, j, i * i * j * random.randint(1, 4))

    bin_edges = list(map(carter, range(ncarter)))
    bins = zip(bin_edges[:-1], bin_edges[1:])

    projections = [br.projection(hist, *bin) for bin in bins]

    # print
    # for b, p in zip(bins, projections):
    # print(b, p.Integral())
    # print(sum(p.Integral() for p in projections), hist.Integral())

    total = sum(p.Integral() for p in projections)
    assert total == hist.Integral()


@pytest.mark.parametrize("wfilename, wselection, whistname", [
    ('test_read.root', 'testSelection', 'testHistogram')
])
def test_read(wfilename, wselection, whistname, write_histogram, stop):
    assert br.io.read(wfilename, wselection, whistname) is not None

    # Now raise exceptions when reading
    # the root file with wrong names
    with pytest.raises(IOError):
        br.io.read('junk' + wfilename, wselection, whistname)
    with pytest.raises(IOError):
        br.io.read(wfilename, 'junk' + wselection, whistname)
    with pytest.raises(IOError):
        br.io.read(wfilename, wselection, 'junk' + whistname)


@pytest.mark.parametrize("wfilename, wselection, whistnames", [
    ('test_read.root', 'testSelection',
        ['testHistogram_{0}'.format(i) for i in range(10)])
])
def test_readmult(written_histograms, wfilename, wselection, whistnames, stop):
    histograms = br.io.read_multiple(wfilename, wselection, whistnames)

    assert histograms is not None
    assert len(histograms) == len(whistnames)
    assert histograms[0] is not None

    # Now feed it with wrong name
    whistnames.append('junk')
    with pytest.raises(IOError):
        br.io.read_multiple(wfilename, wselection, whistnames)


def test_ratio(stop):
    hist1 = ROOT.TH1F("test1", "numerator", 100, -10, 10)
    hist2 = ROOT.TH1F("test2", "denominator", 100, -10, 10)
    hist1.FillRandom("gaus")
    hist1.FillRandom("expo")
    ratio = br.ratio(hist1, hist2)
    assert br.same_binning(ratio, hist1)
    assert br.same_binning(ratio, hist2)


def test_sets_events(stop, nominal_hist):
    nominal_hist.FillRandom("gaus")
    events, integral = 1000, nominal_hist.Integral()

    # No normalization
    br.set_nevents(nominal_hist, events)

    # Check if .nevents attribute is OK
    assert nominal_hist.nevents == events
    # Check if we don't mess with area
    assert nominal_hist.Integral() != integral / events


def test_rebins_proba(stop, edges):
    hist1 = ROOT.TH1F("test", "rebins proba", 200, 0, 20)
    hist1.Sumw2()
    hist1.FillRandom("pol0")
    rebinned = br.rebin_proba(hist1, edges=edges)
    Comparator(stop=stop).compare(hist1, rebinned)
    assert hist1.GetNbinsX() != rebinned.GetNbinsX()

    # Just check if ratio gives warnings
    ratio = br.ratio(rebinned, rebinned)
    assert ratio.GetEntries() > 0


def test_sum(stop):
    hists = [ROOT.TH1F("tt{}".format(i), "", 200, -10, 10) for i in range(10)]

    for hist in hists:
        hist.FillRandom('gaus')

    entries = sum(h.GetEntries() for h in hists)

    newlabel = 'total'
    total = br.hsum(hists, newlabel)
    assert total.GetEntries() == entries


def test_average(stop):
    hists = [ROOT.TH1F("tt{}".format(i), "", 200, -10, 10) for i in range(10)]
    for hist in hists:
        for i in range(10):
            hist.Fill(i, i)
    mean = br.average(hists, label="average")
    assert mean.GetBinContent(1) == hists[0].GetBinContent(1)
    assert mean.GetBinContent(10) == hists[0].GetBinContent(10)
    assert mean.GetBinError(1) == hists[0].GetBinError(1)
    assert mean.GetBinError(10) == hists[0].GetBinError(10)


def test_scales_histogram(nbins=200, hmin=-10, hmax=10):
    hist = ROOT.TH1F("refhistScale", "Testing scalew", nbins, hmin, hmax)

    hist.FillRandom('gaus')

    # Calculate bin width
    binwidth = nbins * 1. / (hmax - hmin)

    # For normal even binning these numbers are the same
    entries, integral = hist.GetEntries(), hist.Integral()
    assert entries == integral

    br.scalew(hist, 1)
    assert entries == hist.GetEntries()
    assert hist.Integral() == integral * binwidth

    # NB: Be careful when applying scalew consecutively
    #     the factors multiply
    br.scalew(hist, 2)
    assert pytest.approx(entries) == hist.GetEntries()
    assert hist.Integral() == integral * binwidth * binwidth * 2


def test_calculates_area_and_error(nbins=10, hmin=0, hmax=10):
    hist = ROOT.TH1F("testarea", "", nbins, hmin, hmax)
    hist.Sumw2()

    for i in range(nbins):
        hist.Fill(i, 1)

    def histarea(a, b):
        return b - a

    # These areas work according to the formula
    test_areas = (0, 10), (5, 10), (0, 0)
    for interval in test_areas:
        area, error = br.area_and_error(hist, *interval)
        true = histarea(*interval)
        assert area == true
        assert error == true ** 0.5

    # NB: ROOT behaviour
    # But these areas don't work according agree with expectations
    # because ROOT takes into account both ends of the interval
    fail_areas = (5, 6), (0, 1), (1, 8)
    for interval in fail_areas:
        area, error = br.area_and_error(hist, *interval)
        true = histarea(*interval)
        assert area != true
        # There is no need to compare errors


@pytest.fixture
def iohist(nominal_hist, oname="testSave.root", selection='testSelection'):
    br.io.save(nominal_hist, oname, selection)
    yield oname, selection, nominal_hist.GetName()
    os.remove(oname)


def test_saves_histogram(iohist, nominal_hist):
    oname, selection, histname = iohist
    assert os.path.isfile(oname)

    ffile = br.io.read(oname, selection, histname)
    assert ffile.GetEntries() == nominal_hist.Integral()
    assert ffile.Integral() == nominal_hist.Integral()


def test_initializes_properties_on_inputs(stop):
    # Just to check if init decorator works as expected
    class Empty(object):

        def __init__(self):
            super(Empty, self).__init__()

        @br.init_inputs
        def identity(self, hists):
            return hists

    inputs = (ROOT.TH1F("tt{}".format(i), "", 200, -10, 10) for i in range(10))
    for hist in inputs:
        hist.FillRandom('gaus')

    for hist in inputs:
        with pytest.raises(AttributeError):
            hist.logy
            hist.logx

    data = Empty()
    outputs = data.identity(inputs)
    # Decorated method takes alrady modified objects
    for hist in inputs:
        hist.logy

    # It's the same objects
    for inp, out in zip(inputs, outputs):
        assert inp is out


def test_initializes_colors(stop):
    ci = br.BR_COLORS
    hists = []
    for i, c in enumerate(ci):
        hist = ROOT.TH1F("hCol{}".format(i), "Test BROOT: Colors", 40, -4, 4)
        hist.FillRandom('gaus')
        hist.Scale(1 + 1. / (i + 1))
        hist.SetLineColor(c)
        hist.SetFillColor(c)
        hist.SetMarkerColor(c)
        hist.SetMarkerStyle(20)
        hists.append(hist)
    Comparator(stop=stop).compare(hists)


def test_caclulates_syst_deviation(stop):
    hists = [ROOT.TH1F("hDev_%d" % i, "%d; x, GeV; y, N" %
                       i, 20, 0, 20) for i in range(10)]

    for i, hist in enumerate(hists):
        for b in br.hrange(hist):
            hist.SetBinContent(b, b)

    hist, rms, mean = br.systematic_deviation(hists)

    for i, m in enumerate(mean):
        assert i + 1 == m

    for r in rms:
        assert r == 0

    hist.SetTitle('TEST BROOT: Check RMS/mean ratio (should be zero)')
    with su.canvas(stop=stop):
        hist.Draw()


def test_extracts_bins(stop):
    hist = ROOT.TH1F("hGetBins", "Test BROOT: Retuns binvalues", 40, 0, 40)
    for i in br.hrange(hist):
        hist.Fill(i - 0.5, i), hist.GetBinContent(i)

    bins, errors, centers, widths = br.bins(hist)
    assert len(bins) == hist.GetNbinsX()
    assert len(errors) == hist.GetNbinsX()

    for i, b in enumerate(bins):
        assert hist.GetBinContent(i + 1) == b

    for b, e in zip(bins, errors):
        assert e == b

    for i, b in enumerate(errors):
        assert hist.GetBinError(i + 1) == b


@pytest.mark.skip("Don't rely on external traffic")
def test_downloads_from_hepdata(stop):
    record, ofile = 'ins1620477', 'test_hepdata.root'

    br.io.hepdata(record, ofile)
    assert os.path.isfile(ofile)

    with br.tfile(ofile) as rfile:
        assert rfile.IsOpen()
    os.remove(ofile)


@pytest.mark.skip("Don't rely on external traffic")
def test_reads_from_tdir(stop):
    record, ofile = 'ins1620477', 'test_hepdata.root'

    br.io.hepdata(record, ofile)
    hist = br.io.read(ofile, 'Table 1', 'Hist1D_y1')
    hist.SetTitle('TEST BROOT: Test read from TDirectory')
    with su.canvas(stop=stop):
        hist.Draw()
    os.remove(ofile)


def test_iterates_over_bins(stop):
    # If fill returns bin number, then it's ok
    # otherwise it returns -1
    #

    hist = ROOT.TH1F(
        "hIterations1", "Test BROOT: Test iterations", 100, -4, 4)
    for i in br.hrange(hist):
        hcenter = hist.GetBinCenter(i)
        assert hist.Fill(hcenter == i), i

    hist = ROOT.TH1F(
        "hIterations2", "Test BROOT: Test iterations", 100, 0, 4000)
    for i in br.hrange(hist):
        hcenter = hist.GetBinCenter(i)
        assert hist.Fill(hcenter == i), i

    hist = ROOT.TH1F(
        "hIterations2", "Test BROOT: Test iterations", 4, 0, 4)
    for i in br.hrange(hist):
        hcenter = hist.GetBinCenter(i)
        assert hist.Fill(hcenter == i), i


def test_returns_func_parameters(stop):
    func = ROOT.TF1('h', '[1] * x * x  + [0] * x + [2]', 0, 10)
    parameters = 1, 2, 3
    func.SetParameters(*parameters)

    pars, errors = br.pars(func)

    for pair in zip(pars, parameters):
        assert pair[0] == pair[1]
    pars, _ = br.pars(func, 2)

    for pair in zip(pars, parameters[0:2]):
        assert pair[0] == pair[1]


def test_diffs_histograms(stop):
    hist = ROOT.TH1F("hDiff", "Test BROOT: Test iterations", 100, -4, 4)
    hist.FillRandom('gaus')

    assert br.diff(hist, hist)

    cloned = br.clone(hist)
    assert br.diff(hist, cloned)

    # NB: This test will pass as this value
    # doesn't exceed default tolerance
    cloned.Fill(0, 1e-9)
    assert br.diff(hist, cloned)

    cloned.Fill(0, 1e-5)
    assert not br.diff(hist, cloned)


def test_sets_to_zero(stop):
    hist1 = ROOT.TH1F("test", "Test BROOT1: Test add Trimm", 100, -4, 4)
    hist1.SetLineColor(46)
    for b in br.hrange(hist1):
        hist1.SetBinContent(b, - 2 * hist1.GetBinCenter(b) - 1)

    zero_range = (-1, 4)
    bin_range = map(hist1.FindBin, zero_range)

    hist1.Sumw2()
    with su.canvas(stop=stop):
        hist1.Draw()

    br.set_to_zero(hist1, zero_range)
    with su.canvas(stop=stop):
        hist1.Draw()

    a, b = bin_range
    for i in range(1, hist1.GetNbinsX()):
        if a - 1 < i < b:
            continue
        assert hist1.GetBinContent(i) == 0


def test_sum_trimm(stop):
    hist1 = ROOT.TH1F("hAdd1", "Test BROOT1: Test add Trimm", 100, -4, 4)
    hist1.SetLineColor(46)
    for i in br.hrange(hist1):
        hist1.SetBinContent(i, - 2 * hist1.GetBinCenter(i) - 1)

    hist2 = ROOT.TH1F("hAdd2", "Test BROOT2: Test add Trimm", 100, -4, 4)
    hist2.SetLineColor(37)
    for i in br.hrange(hist2):
        hist2.SetBinContent(i, hist2.GetBinCenter(i))

    hists = hist1, hist2
    ranges = (-4, -0.5), (-0.5, 4)
    hist = br.sum_trimm(hists, ranges)

    with su.canvas(stop=stop):
        hist.Draw()
        hist1.Draw("same")
        hist2.Draw("same")

    for hh, rr in zip(hists, ranges):
        a, b = map(hist.FindBin, rr)
        for i in range(1, hh.GetNbinsX()):
            if a < i < b - 1:
                assert hh.GetBinContent(i), hist.GetBinContent(i)
                # print(hh.GetBinContent(i), hist.GetBinContent(i))


def test_calculates_confidence_intervals(stop):
    hist1 = ROOT.TH1F("hFit", "Test BROOT: Trimm", 100, -4, 4)
    hist1.FillRandom("gaus")
    function = ROOT.gROOT.FindObject("gaus")
    ci = br.confidence_intervals(hist1, function)

    assert hist1.GetNbinsX() == ci.GetNbinsX()
    assert hist1.GetEntries() != 0


def test_chi2(stop):
    histogram = ROOT.TH1F("TestChi2", "Test BROOT: chi2", 100, -1, 1)
    histogram.Sumw2()
    histogram.FillRandom("gaus")
    # assert br.chi2(histogram == histogram), 0

    histogram2 = br.clone(histogram)
    error = histogram2.GetBinError(1)
    histogram2.SetBinContent(1, histogram2.GetBinContent(1) + error)
    # The sigma of this datapoint drops as 1 / sqrt(2)
    # because both points have their own errors
    assert pytest.approx(br.chi2(histogram, histogram2)) == 0.5


def test_scales_with_rebins(stop):
    hist1 = ROOT.TH1F(
        "TestScalesAndRebins",
        "Test Scales and rebins",
        1000, 0, 20
    )
    function = ROOT.TF1('exp', "TMath::Exp(-[0] * x) * [1] ", 0, 20)
    function.SetParameters(0.5, 1000000)

    for i in br.hrange(hist1):
        value = function.Eval(hist1.GetBinCenter(i))
        hist1.SetBinContent(i, value)
    pt = Options().pt.ptedges

    hist1.Draw()
    # hist1.logy = True
    hist1.Sumw2()
    hist1.label = "original"
    hist2 = hist1.Rebin(
        len(pt) - 1,
        hist1.GetName() + "_copy",
        array.array('d', pt)
    )
    hist2.Draw("same")
    hist2.label = "rebinned"
    Comparator(stop=stop).compare(hist1, hist2)
    hist3 = hist2.Clone(hist2.GetName() + "_scale")
    br.scalew(hist3, hist1.GetBinWidth(0))
    Comparator(stop=stop).compare([hist1, hist2, hist3])


@pytest.fixture
def exp_data():
    with open("config/pt.json") as f:
        data = array.array('d', json.load(f)["#pi^{0}"].get("ptedges"))
    hist = ROOT.TH1F("random", "Testing bin centers; x", len(data) - 1, data)
    function = ROOT.TF1("function", "TMath::Exp(-0.5 * x)", 0, 100)
    hist.FillRandom(function.GetName())
    return br.scalew(hist)


def test_calculates_bin_centers(exp_data):
    centers = br.bin_centers(exp_data)
    orig_contents, orig_errors, orig_centers, _ = br.bins(exp_data)
    cent_contents, cent_errors, cent_centers, _ = br.bins(centers)

    np.testing.assert_almost_equal(orig_centers, cent_centers)
    np.testing.assert_almost_equal(orig_centers, cent_contents)
    np.testing.assert_almost_equal(cent_errors, np.zeros_like(cent_errors))


def test_calculates_ratio_bin_centers(exp_data):
    normalized = br.divide_by_bin_centers(exp_data)
    assert normalized is not exp_data


def test_retrieves_edges():
    edges_nominal = array.array('d', [0, 1, 2, 3, 4, 5, 10, 100])
    hist = ROOT.TH1F("h", "hist", len(edges_nominal) - 1, edges_nominal)
    edges = br.edges(hist)
    assert len(edges_nominal) == len(edges)

    np.testing.assert_almost_equal(edges_nominal, edges)


def test_graph_asym_error(stop):
    x = np.arange(100)
    y = np.e ** (-np.arange(100) / 100)
    ex = np.zeros_like(x)
    ey = y * 0.001
    graph = ROOT.TGraphAsymmErrors(
        len(x),
        array.array('d', x),
        array.array('d', y),
        array.array('d', ex),
        array.array('d', ey),
    )

    hist = ROOT.TH1F("hist", "test", 100, 0, 100)
    br.graph2hist(graph, hist)

    with su.canvas(stop=stop):
        graph.Draw("APL")
        hist.SetLineColor(ROOT.kRed + 1)
        hist.Draw("same")

    br.graph2hist(graph)


def test_hist2graph(stop):
    hist = ROOT.TH1F("hist", "test", 100, -3, 3)
    hist.FillRandom("gaus")
    graph = br.hist2graph(hist)

    with su.canvas(stop=stop):
        graph.Draw("APL")
        hist.SetLineColor(ROOT.kRed + 1)
        hist.Draw("same")


def test_plots_shaded_area(stop):
    sin = ROOT.TF1("low", "sin(x)", np.pi / 4, 1 * np.pi + np.pi / 4)
    cos = ROOT.TF1("high", "cos(x)", np.pi / 4, np.pi + np.pi / 4)
    shaded = br.shaded_region("test hysteresis", sin, cos)
    with su.canvas(stop=stop):
        shaded.Draw(shaded.GetDrawOption())


def test_modulenames(n_modules=4, max_combinations=7):
    assert len(br.module_names(same_module=True)) == n_modules
    assert len(br.module_names(same_module=False)) == max_combinations


def test_chi2ndf(nominal_hist):
    hist = nominal_hist.Clone("test_chi2ndf")
    for i in br.hrange(hist):
        hist.SetBinError(i, 1)
    assert br.chi2ndf(hist, hist) == 0.0


def test_chi2ndf_function():
    func = ROOT.TF1("high", "[0] * cos(x[0])", 0, 10)
    assert br.chi2ndf(func) == 0.0
