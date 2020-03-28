import os
import pytest
import tqdm

from spectrum.vault import AnalysisInput
from spectrum.pipeline import AnalysisDataReader
from spectrum.vault import DataVault
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


@pytest.fixture()
def multihist_input():
    return lambda i, j: DataVault().input(
        "single #pi^{0}", "high",
        listname="PhysNonlinScan",
        histname="MassPt_{}_{}".format(i, j))


@pytest.mark.onlylocal
@pytest.mark.skip("These tests are only needed to check memory consumption")
def test_sequence(multihist_input, sbins=(11, 11)):
    x, y = sbins
    for i in range(x):
        for j in range(y):
            hists = multihist_input(i, j)
            assert hists is not None


@pytest.mark.onlylocal
@pytest.mark.skip("These tests are only needed to check memory consumption")
def test_copy(multihist_input):
    raw, mixed = multihist_input(0, 0).read()
    cache = []
    msize = 11 * 11
    for i in tqdm.tqdm(range(msize)):
        hists = raw.Clone(), mixed.Clone()
        cache.append(hists)
