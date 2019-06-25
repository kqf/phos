from __future__ import print_function
import array
import os
import random

import pytest
import ROOT

from spectrum.broot import BROOT as br
from spectrum.comparator import Comparator
from spectrum.options import Options
from spectrum.sutils import wait


# NB: Don't use broot in write functions
#     as it's important to test without broot
#

@pytest.fixture
def edges(settings):
    return settings["test_broot"]["edges"]


def write_histogram(filename, selection, histname):
    hist = br.BH(
        ROOT.TH1F, histname,
        'Testing reading histograms from a rootfile',
        10, -3, 3)
    hist.FillRandom('gaus')
    tlist = ROOT.TList()
    tlist.SetOwner(True)
    tlist.Add(hist)

    ofile = ROOT.TFile(filename, 'recreate')
    tlist.Write(selection, 1)
    ofile.Close()
    return br.clone(hist)


def write_histograms(filename, selection, histnames):
    hists = [br.BH(
        ROOT.TH1F, histname,
        'Testing reading histograms from a rootfile',
        10, -3, 3)
        for histname in histnames
    ]

    for hist in hists:
        hist.FillRandom('gaus')

    tlist = ROOT.TList()
    tlist.SetOwner(True)
    map(tlist.Add, hists)

    ofile = ROOT.TFile(filename, 'recreate')
    tlist.Write(selection, 1)
    ofile.Close()
    return map(br.clone, hists)


@pytest.fixture(scope="module")
def testhist():
    testhist = br.BH(
        ROOT.TH1F, "hist" + str(random.randint(0, 1e9)),
        "Testing creating of the histogram", 100, -10, 10,
        label='test')
    testhist.FillRandom("gaus")
    return testhist


def test_properties(stop, testhist):
    for p in br.prop._properties.keys():
        assert p in dir(testhist)


def test_draw(stop, testhist):
    assert testhist is not None
    testhist.Draw()
    wait(stop=stop)


def test_setp(stop, testhist):
    hist = ROOT.TH1F(
        "refhistSet",
        "Testing set_property method",
        100, -10, 10)

    # Set properties of root object
    br.setp(hist, testhist)

    assert br.same(hist, testhist)


def test_clone_from_root(stop):
    hist = br.BH(
        ROOT.TH1F, "refhistROOT", "Testing set_property method",
        100, -10, 10)

    hist2 = br.BH(
            ROOT.TH1F, hist)

    # Properties should not copy when using copy constructor
    #
    assert br.prop.has_properties(hist2)


def test_clone(stop):
    hist = br.BH(
        ROOT.TH1F,
        "refhistClone",
        "Testing updated Clone method", 100, -10, 10,
        label="test prop", logy=True, logx=False, priority=3)

    hist.FillRandom("gaus")

    # NB: There is no need to manually set properties
    hist2 = br.clone(hist)

    # Copy differs clone
    assert hist.GetEntries() == hist2.GetEntries()

    # Now copy the properties
    assert br.same(hist2, hist)


def test_copy(stop):
    hist = br.BH(
        ROOT.TH1F,
        "refhistCopy",
        "Testing updated Clone method", 100, -10, 10,
        label="test prop", logy=True, logx=False, priority=3)

    hist.FillRandom("gaus")

    # NB: There is no need to manually set properties
    # Now try copy instead of clone
    hist2 = br.copy(hist)

    # Copy differs clone
    # These should not equal
    assert not hist.GetEntries() == hist2.GetEntries()

    # Now copy the properties
    assert br.same(hist2, hist)


def test_bh2_draws_projection_range(stop):
    hist = br.BH(
        ROOT.TH2F, "refhistProj",                  # Name
        "Testing updated ProjectX method for BH2F",  # Title
        100, 20, 30, 100, -10, 10,                 # Xbins, Ybins
        label="test prop",                        # Label
        logy=1, logx=0, priority=3            # Misc properties
    )

    # Fill random values
    for i in br.range(hist):
        for j in br.range(hist, 'y'):
            hist.SetBinContent(i, j, i * i * j * random.randint(1, 4))

    hist.Draw('colz')
    wait(stop=stop)

    # NB: There is no need to manually set properties
    hist2 = br.project_range(hist, 'newname', -5, 5)

    hist2.Draw()
    wait(stop=stop)

    # Now copy the properties
    assert br.same(hist2, hist)


def test_projection_saves_area(stop):
    # NB: Bin according to this sequence https://oeis.org/A000124
    #     so the bin width of a projection hist always increases
    #
    carter, ncarter = lambda n: n * (n + 1) / 2 + 1, 16

    # TODO: figure out what is why do we should nbinsx, not nbinsy
    #       this contradicts regular logic

    nbinsx, startx, stopx = carter(ncarter), -10, 10
    nbinsy, starty, stopy = 100, -10, 10

    hist = br.BH(
        ROOT.TH2F,
        "refhistProjArea",  # Name
        "Testing updated ProjectX method for BH2F",   # Title
        nbinsx, startx, stopx, nbinsy,
        starty, stopy,  # Xbins, Ybins
        label="test prop",  # Label
        logy=1, logx=0, priority=3  # Misc properties
    )

    # Fill random values
    for i in br.range(hist):
        for j in br.range(hist, 'y'):
            hist.SetBinContent(i, j, i * i * j * random.randint(1, 4))

    bin_edges = map(carter, range(ncarter))
    bins = zip(bin_edges[:-1], bin_edges[1:])

    projections = [br.projection(hist, "%d_%d", *bin) for bin in bins]

    # print
    # for b, p in zip(bins, projections):
    # print(b, p.Integral())
    # print(sum(p.Integral() for p in projections), hist.Integral())

    total = sum(p.Integral() for p in projections)
    assert total == hist.Integral()


def test_read(stop):
    data = 'test_read.root', 'testSelection', 'testHistogram'
    write_histogram(*data)
    assert br.io.read(*data) is not None

    # Now raise exceptions when reading
    # the root file with wrong names
    with pytest.raises(IOError):
        br.io.read('junk' + data[0], data[1], data[2])
    with pytest.raises(IOError):
        br.io.read(data[0], 'junk' + data[1], data[2])
    with pytest.raises(IOError):
        br.io.read(data[0], data[1], 'junk' + data[2])
    os.remove(data[0])


def test_read_multiple(stop):
    ofilename = 'test_read.root'
    selection = 'testSelection'
    histnames = ['testHistogram_{0}'.format(i) for i in range(10)]

    write_histograms(ofilename, selection, histnames)

    histograms = br.io.read_multiple(ofilename, selection, histnames)
    assert histograms is not None
    assert len(histograms) == len(histnames)
    assert histograms[0] is not None

    # Now feed it with wrong name
    histnames.append('junk')
    with pytest.raises(IOError):
        br.io.read_multiple(ofilename, selection, histnames)
    os.remove(ofilename)


def test_ratio(stop):
    hist1 = br.BH(
        ROOT.TH1F,
        "refhistRatio1",
        "Testing the ratio method", 100, -10, 10,
        label="test ratio", logy=True, logx=False, priority=3)

    hist2 = br.BH(
        ROOT.TH1F,
        "refhistRatio2",
        "Testing the ratio method", 100, -10, 10,
        label="test ratio b", logy=True, logx=False, priority=3)

    hist1.FillRandom("gaus")
    hist1.FillRandom("expo")
    ratio = br.ratio(hist1, hist2)

    # Check if the numerator and the ratio are the same
    assert br.same(hist1, ratio)

    # Check if the numerator and the ratio are not same
    assert not br.same(hist2, ratio)


def test_sets_events(stop):
    hist1 = br.BH(
            ROOT.TH1F,
        "refhistSetEvents", "Testing set events", 100, -10, 10,
        label="test ratio", logy=True, logx=False, priority=3)

    hist1.FillRandom("gaus")
    events, integral = 1000, hist1.Integral()

    # No normalization
    br.set_nevents(hist1, events)

    # Check if .nevents attribute is OK
    assert hist1.nevents == events
    # Check if we don't mess with area
    assert hist1.Integral() != integral / events

    # Now with normalization
    br.set_nevents(hist1, events, True)
    # Check if .nevents attribute is OK
    assert hist1.nevents == events
    # Check if we don't mess with area
    assert abs(hist1.Integral() - integral / events) < 0.001


def test_rebins_proba(stop, edges):
    hist1 = br.BH(
            ROOT.TH1F,
        "refhistRebinProba1", "Testing rebins proba", 200, 0, 20,
        label="test ratio", logy=True, logx=False, priority=3)
    hist1.Sumw2()
    hist1.FillRandom("pol0")
    rebinned = br.rebin_proba(hist1, edges=edges)
    Comparator(stop=stop).compare(hist1, rebinned)
    assert hist1.GetNbinsX() != rebinned.GetNbinsX()

    # Just check if ratio gives warnings
    ratio = br.ratio(rebinned, rebinned)
    assert br.same(rebinned, hist1)
    assert ratio.GetEntries()


def test_rebins(stop):
    hist1 = br.BH(
            ROOT.TH1F,
        "refhistRebin1", "Testing rebins", 200, -10, 10,
        label="test ratio", logy=True, logx=False, priority=3)

    hist2 = br.BH(
            ROOT.TH1F,
        "refhistRebin2", "Testing rebins", 100, -10, 10,
        label="test ratio", logy=True, logx=False, priority=3)

    hist1.FillRandom("gaus")
    hist2.FillRandom("gaus")

    rebinned, hist2 = br.rebin_as(hist1, hist2)

    assert hist1.GetNbinsX() != hist2.GetNbinsX()

    assert rebinned.GetNbinsX() == hist2.GetNbinsX()

    # Just check if ratio gives warnings
    ratio = br.ratio(rebinned, hist2)
    assert br.same(rebinned, hist1)
    assert ratio.GetEntries()


def test_sum(stop):
    hists = [br.BH(
        ROOT.TH1F,
        "refhistSum_%d" % i, "Testing sum %d" % i, 200, -10, 10,
        label="%dth histogram" % i, logy=True, logx=False, priority=3)
        for i in range(10)]

    for hist in hists:
        hist.FillRandom('gaus')

    entries = sum(h.GetEntries() for h in hists)

    newlabel = 'total'
    total = br.sum(hists, newlabel)

    assert total.GetEntries() == entries
    assert total.label == newlabel


def test_average(stop):
    hists = [br.BH(
        ROOT.TH1F,
        "refhistSum_%d" % i, "Testing sum %d" % i, 200, -10, 10,
        label="%dth histogram" % i, logy=True, logx=False, priority=3)
        for i in range(10)]

    for hist in hists:
        for i in range(10):
            hist.Fill(i, i)

    newlabel = 'average'
    total = br.sum(hists, newlabel)
    assert total.GetBinContent(1) == hists[0].GetBinContent(1)
    assert total.GetBinContent(10) == hists[0].GetBinContent(10)
    assert total.GetBinError(1) == hists[0].GetBinError(1)
    assert total.GetBinError(10) == hists[0].GetBinError(10)


def test_scales_histogram(stop):
    nbins, start, stop = 200, -10, 10

    hist = br.BH(
        ROOT.TH1F,
        "refhistScale", "Testing scalew", nbins, start, stop,
        label="scale", logy=True, logx=False, priority=3)

    hist.FillRandom('gaus')

    # Calculate bin width
    binwidth = nbins * 1. / (stop - start)

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


def test_scales_for_binwith(stop):
    nbins, start, stop = 200, -10, 10

    hist = br.BH(
        ROOT.TH1F,
        "refhistScale", "Testing scalew", nbins, start, stop,
        label="scale", logy=True, logx=False, priority=3)

    hist.FillRandom('gaus')

    # Calculate bin width
    binwidth = nbins * 1. / (stop - start)

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


def test_calculates_area_and_error(stop):
    nbins, start, stop = 10, 0, 10
    hist = br.BH(
        ROOT.TH1F,
        "refhistAreaError", "Testing area and error", nbins, start, stop,
        label="scale", logy=True, logx=False, priority=3)
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


def test_saves_histogram(stop):
    oname, selection, histname = (
        'testSave.root', 'testSelection', 'refhistSave')

    hist = br.BH(
        ROOT.TH1F,
        histname, "Testing scalew", 200, -10, 10,
        label="scale", logy=True, logx=False, priority=3)
    hist.FillRandom('gaus')
    integral = hist.Integral()
    entries = hist.GetEntries()

    br.io.save(hist, oname, selection)

    # It's important to check if we don't delete
    # the hist accidentally
    assert hist is not None

    assert os.path.isfile(oname)

    ffile = br.io.read(oname, selection, histname)
    assert ffile.GetEntries() == entries
    assert ffile.Integral() == integral
    os.remove(oname)


def test_initializes_inputs(stop):
    # Just to check if init decorator works as expected
    class Empty(object):

        def __init__(self):
            super(Empty, self).__init__()

        @br.init_inputs
        def identity(self, hists):
            return hists

    inputs = (ROOT.TH1F("hTestInitMultiple%d" % i,
                        "Testing sum %d" % i, 200, -10, 10)
              for i in range(10))

    for hist in inputs:
        hist.FillRandom('gaus')

    # There is no porperties
    for hist in inputs:
        assert not br.prop.has_properties(hist)

    data = Empty()
    outputs = data.identity(inputs)

    # Decorated method takes alrady modified objects
    for hist in outputs:
        assert br.prop.has_properties(hist)

    # It's the same objects
    for inp, out in zip(inputs, outputs):
        assert inp is out


def test_initializes_colors(stop):
    ci = br.define_colors()
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
        for b in br.range(hist):
            hist.SetBinContent(b, b)

    hist, rms, mean = br.systematic_deviation(hists)

    for i, m in enumerate(mean):
        assert i + 1 == m

    for r in rms:
        assert r == 0

    hist.SetTitle('TEST BROOT: Check RMS/mean ratio (should be zero)')
    hist.Draw()
    wait(stop=stop)


def test_extracts_bins(stop):
    hist = ROOT.TH1F("hGetBins", "Test BROOT: Retuns binvalues", 40, 0, 40)
    for i in br.range(hist):
        hist.Fill(i - 0.5, i), hist.GetBinContent(i)

    bins, errors, centers = br.bins(hist)
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

    rfile = br.io._read_file(ofile)
    assert rfile.IsOpen()
    os.remove(ofile)


@pytest.mark.skip("Don't rely on external traffic")
def test_reads_from_tdir(stop):
    record, ofile = 'ins1620477', 'test_hepdata.root'

    br.io.hepdata(record, ofile)
    hist = br.io.read(ofile, 'Table 1', 'Hist1D_y1')
    hist.SetTitle('TEST BROOT: Test read from TDirectory')
    hist.Draw()
    wait(stop=stop)
    os.remove(ofile)


def test_iterates_over_bins(stop):
    # If fill returns bin number, then it's ok
    # otherwise it returns -1
    #

    hist = ROOT.TH1F(
        "hIterations1", "Test BROOT: Test iterations", 100, -4, 4)
    for i in br.range(hist):
        hcenter = hist.GetBinCenter(i)
        assert hist.Fill(hcenter == i), i

    hist = ROOT.TH1F(
        "hIterations2", "Test BROOT: Test iterations", 100, 0, 4000)
    for i in br.range(hist):
        hcenter = hist.GetBinCenter(i)
        assert hist.Fill(hcenter == i), i

    hist = ROOT.TH1F(
        "hIterations2", "Test BROOT: Test iterations", 4, 0, 4)
    for i in br.range(hist):
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
    hist1 = br.BH(ROOT.TH1F, "hAddTrimm1",
                  "Test BROOT1: Test add Trimm", 100, -4, 4)
    hist1.label = 'Remove this label later'
    hist1.SetLineColor(46)
    for bin in br.range(hist1):
        hist1.SetBinContent(bin, - 2 * hist1.GetBinCenter(bin) - 1)

    zero_range = (-1, 4)
    bin_range = map(hist1.FindBin, zero_range)

    hist1.Sumw2()
    hist1.Draw()
    wait(stop=stop)

    br.set_to_zero(hist1, zero_range)
    hist1.Draw()
    wait(stop=stop)

    a, b = bin_range
    for bin in range(1, hist1.GetNbinsX()):
        # TODO: Check this condition range
        if a - 1 < bin < b:
            continue

        # print(a, bin, b, hist1.GetBinContent(bin))
        assert hist1.GetBinContent(bin) == 0


def test_sum_trimm(stop):
    hist1 = br.BH(ROOT.TH1F, "hAddTrimm1",
                  "Test BROOT1: Test add Trimm", 100, -4, 4)
    hist1.label = 'Remove this label later'
    hist1.SetLineColor(46)
    for bin in br.range(hist1):
        hist1.SetBinContent(bin, - 2 * hist1.GetBinCenter(bin) - 1)

    hist2 = br.BH(ROOT.TH1F, "hAddTrimm2",
                  "Test BROOT2: Test add Trimm", 100, -4, 4)
    hist2.label = 'Remove this label later'
    hist2.SetLineColor(37)
    for bin in br.range(hist2):
        hist2.SetBinContent(bin, hist2.GetBinCenter(bin))

    hists = hist1, hist2
    ranges = (-4, -0.5), (-0.5, 4)
    hist = br.sum_trimm(hists, ranges)

    hist.Draw()
    hist1.Draw("same")
    hist2.Draw("same")

    for hh, rr in zip(hists, ranges):
        a, b = map(hist.FindBin, rr)
        for bin in range(1, hh.GetNbinsX()):
            if a < bin < b - 1:
                assert hh.GetBinContent(bin), hist.GetBinContent(bin)
                # print(hh.GetBinContent(bin), hist.GetBinContent(bin))

    wait(stop=stop)


def test_calculates_confidence_intervals(stop):
    hist1 = br.BH(ROOT.TH1F, "hFit", "Test BROOT: Trimm", 100, -4, 4)
    hist1.FillRandom("gaus")
    function = ROOT.gROOT.FindObject("gaus")

    ci = br.confidence_intervals(hist1, function)

    assert hist1.GetNbinsX() == ci.GetNbinsX()
    assert hist1.GetEntries() != 0


def test_subtracts_histogram(stop):
    hist = br.BH(ROOT.TH1F, "f2h", "Test BROOT: func2hist", 100, -4, 4)
    for b in br.range(hist):
        hist.Fill(hist.GetBinCenter(b), 5)
    func = ROOT.TF1("testFunc", "5", -4, 4)
    output = br.function2histogram(func, hist)
    output.Add(hist, -1)
    assert output.Integral() == 0


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

    for i in br.range(hist1):
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


@pytest.mark.parametrize("scale", [0.001, 0.1, 1., 10, 100])
def test_draws_chi2(scale):
    hist = ROOT.TH1F("testchi2plot", "Testing #chi^{2} plot; x", 10, 0, 10)
    for i in br.range(hist):
        hist.SetBinContent(i, 1.)
        hist.SetBinError(i, 0.1)
    hist.SetBinContent(5, 2)

    func = ROOT.TF1("func", "pol0", 0, 10)
    func.SetParameter(0, 1)
    hist.Fit(func, "RQ")
    hist = br.chi2errors(hist, scale=scale)
    calculated = sum(map(hist.GetBinError, br.range(hist)))
    assert pytest.approx(calculated) == func.GetChisquare() * scale
