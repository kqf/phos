import pytest

from spectrum.vault import AnalysisInput
from spectrum.pipeline import AnalysisDataReader


@pytest.mark.parametrize("wfilename, wselection, whistnames", [
    ('test.root', 'testSelection', ["hMassPt", "hMixMassPt", "EventCounter"])
])
def test_reads_standard(written_histograms, wfilename, wselection, whistnames):
    oreal, omixed, ocntr = written_histograms
    data = AnalysisInput(wfilename, wselection)
    (real, mixed), pt_range = AnalysisDataReader().transform(data, None)
    assert real is not None
    assert mixed is not None
    assert real.GetEntries() == oreal.GetEntries()
    assert mixed.GetEntries() == omixed.GetEntries()
    assert real.nevents == ocntr.GetBinContent(2)
    assert real.nevents == mixed.nevents


@pytest.mark.parametrize("wfilename, wselection, whistnames", [
    ('test.root', 'testNoMixingSelection', ["hMassPt", "EventCounter"])
])
def test_reads_nomixing_input(written_histograms, wfilename, wselection):
    oreal, ocntr = written_histograms
    data = AnalysisInput(wfilename, wselection, suffixes=None)
    real = next(iter(AnalysisDataReader().transform(data, None)))
    assert real[0] is not None
    assert real[0].GetEntries() == oreal.GetEntries()
    assert real[0].nevents == ocntr.GetBinContent(2)
