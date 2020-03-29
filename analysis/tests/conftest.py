import ROOT

import os
import sys
import pytest

import spectrum.broot as br


@pytest.fixture
def stop():
    not_discover = 'discover' not in sys.argv
    not_pytest = 'pytest' not in sys.argv[0]
    return not_discover and not_pytest


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "onlylocal: mark test to run only as they require the data ",
    )
    config.addinivalue_line(
        "markers",
        "interactive: exclude scripts with ROOT pop-up windows",
    )
    config.addinivalue_line(
        "markers",
        "thesis: script produces the final images",
    )


# TODO: Fix wfilename ... etc.
@pytest.fixture
def written_histograms(wfilename, wselection, whistnames):
    hists = [ROOT.TH1F(histname, '', 10, -3, 3) for histname in whistnames]

    tlist = ROOT.TList()
    tlist.SetOwner(True)
    for hist in hists:
        hist.FillRandom('gaus')
        tlist.Add(hist)

    with br.tfile(wfilename, "recreate"):
        tlist.Write(wselection, ROOT.TObject.kSingleKey)
    yield list(map(br.clone, hists))
    os.remove(wfilename)
