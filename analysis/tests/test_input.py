import os
import pytest

from spectrum.vault import AnalysisInput
from spectrum.pipeline import AnalysisDataReader
# TODO: Fix me
from tests.test_broot import write_histograms


@pytest.fixture(scope="module")
def single():
    ofilename = "test_reads_single.root"
    selection = "testSelection"
    myhist = "testHistogram"
    histnames = myhist, "EventCounter"
    original = write_histograms(ofilename, selection, histnames)
    yield original, ofilename, selection, histnames, myhist
    os.remove(ofilename)


@pytest.fixture(scope="module")
def standard():
    ofilename = "test_reads_standard.root"
    selection = "testSelection"
    histnames = "hMassPt", "hMixMassPt", "EventCounter"
    oreal, omixed, ocntr = write_histograms(ofilename, selection, histnames)
    yield oreal, omixed, ocntr, ofilename, selection, histnames
    os.remove(ofilename)


@pytest.fixture(scope="module")
def nomixing():
    ofilename = "test_reads_nomixing.root"
    selection = "testSelection"
    histnames = "hMassPt", "EventCounter"
    oreal, ocntr = write_histograms(ofilename, selection, histnames)
    yield oreal, None, ocntr, ofilename, selection, histnames
    os.remove(ofilename)


def test_reads_standard_input(standard):
    oreal, omixed, ocntr, ofilename, selection, histnames = standard
    data = AnalysisInput(ofilename, selection)
    (real, mixed), pt_range = AnalysisDataReader().transform(data, None)
    assert real is not None
    assert mixed is not None
    assert real.GetEntries() == oreal.GetEntries()
    assert mixed.GetEntries() == omixed.GetEntries()
    assert real.nevents == ocntr.GetBinContent(2)
    assert real.nevents == mixed.nevents


def test_reads_nomixing_input(nomixing):
    oreal, omixed, ocntr, ofilename, selection, histnames = nomixing
    data = AnalysisInput(ofilename, selection, suffixes=None)
    real = next(iter(AnalysisDataReader().transform(data, None)))
    assert real[0] is not None
    assert real[0].GetEntries() == oreal.GetEntries()
    assert real[0].nevents == ocntr.GetBinContent(2)
