import os
import pytest
import unittest
import tqdm

from spectrum.input import Input, NoMixingInput, read_histogram
from tests.software.test_broot import write_histograms


# TOOD: Add fixtures for these methods

def test_reads_single_histogram():
    ofilename = "test_reads_single.root"
    selection = "testSelection"
    myhist = "testHistogram"
    histnames = myhist, "EventCounter"
    original = write_histograms(ofilename, selection, histnames)

    fromfile = read_histogram(ofilename, selection, myhist)

    assert fromfile is not None
    # We are reading different histograms
    assert fromfile is not original[0]

    # And those histograms have the same name
    fromfile.GetEntries() == original[0].GetEntries()
    os.remove(ofilename)


def test_reads_standard_input():
    ofilename = "test_reads_standard.root"
    selection = "testSelection"
    histnames = "hMassPt", "hMixMassPt", "EventCounter"

    oreal, omixed, cntr = write_histograms(ofilename, selection, histnames)
    onevents = cntr.GetBinContent(2)

    real, mixed = Input(ofilename, selection).read()

    assert real is not None
    assert mixed is not None

    # We are reading different histograms
    assert real is not oreal
    assert mixed is not omixed

    # And those histograms have the same name
    real.GetEntries() == oreal.GetEntries()
    mixed.GetEntries() == omixed.GetEntries()

    real.nevents == onevents
    real.nevents == mixed.nevents
    os.remove(ofilename)

    def test_reads_nomixing_input():
        ofilename = "test_reads_nomixing.root"
        selection = "testSelection"
        histnames = "hMassPt", "EventCounter"

        original = write_histograms(ofilename, selection, histnames)
        oreal, onevents = original[0], original[-1].GetBinContent(2)

        real, mixed = NoMixingInput(ofilename, selection).read()

        assert real is not None
        assert mixed is None

        # We are reading different histograms
        assert real is not oreal

        # And those histograms have the same name
        real.GetEntries() == oreal.GetEntries()

        real.nevents == onevents
        os.remove(ofilename)


# TODO: Update input
class TestInputMemoryPerformance(unittest.TestCase):

    def setUp(self):
        self.infile = "Pythia-new.root"
        self.sel = "StudyNonlinOnlyTender"
        self.hname = "MassPt_%d_%d"
        self.sbins = 11, 11

    @pytest.mark.onlylocal
    @unittest.skip("These tests are only needed to check memory consumption")
    def test_sequence(self):
        x, y = self.sbins
        for i in range(x):
            for j in range(y):
                hists = Input(
                    self.infile,
                    self.sel, self.hname % (i, j)).read()
                assert hists is not None

    @pytest.mark.onlylocal
    @unittest.skip("These tests are only needed to check memory consumption")
    def test_copy(self):
        inp = Input(self.infile, self.sel, self.hname % (0, 0))
        raw, mixed = inp.read()

        cache = []
        msize = 11 * 11
        for i in tqdm.tqdm(range(msize)):
            hists = raw.Clone(), mixed.Clone()
            cache.append(hists)
