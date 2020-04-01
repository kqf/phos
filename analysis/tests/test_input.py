import pytest

from spectrum.vault import AnalysisInput
from spectrum.pipeline import AnalysisDataReader


@pytest.mark.parametrize("filename, selection, histnames", [
    ('test.root', 'testSelection', ["hMassPt", "hMixMassPt", "EventCounter"])
])
def test_reads_standard(written_histograms, filename, selection, histnames):
    oreal, omixed, ocntr = written_histograms
    data = AnalysisInput(filename, selection)
    (real, mixed), pt_range, nev = AnalysisDataReader().transform(data, None)
    assert real is not None
    assert mixed is not None
    assert real.GetEntries() == oreal.GetEntries()
    assert mixed.GetEntries() == omixed.GetEntries()
    assert nev == ocntr.GetBinContent(2)


@pytest.mark.parametrize("filename, selection, histnames", [
    ('test.root', 'testNoMixingSelection', ["hMassPt", "EventCounter"])
])
def test_reads_nomixing_input(written_histograms, filename, selection):
    oreal, ocntr = written_histograms
    data = AnalysisInput(filename, selection, suffixes=None)
    real = next(iter(AnalysisDataReader().transform(data, None)))
    assert real[0] is not None
    assert real[0].GetEntries() == oreal.GetEntries()
