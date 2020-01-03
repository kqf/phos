import ROOT
import json
import pytest
import numpy as np
from math import exp
import array

from spectrum.pipeline import RebinTransformer
from spectrum.output import open_loggs
from spectrum.comparator import Comparator
import spectrum.broot as br
from spectrum.pipeline import SingleHistReader

from vault.datavault import DataVault


@pytest.fixture
def stop():
    return False


@pytest.fixture
def edges(etype):
    if etype == "normal":
        return np.linspace(0, 20, 200)

    with open("config/pt.json") as f:
        data = json.load(f)
    return data["#pi^{0}"]["ptedges"]


@pytest.fixture
def edges_eta():
    with open("config/pt.json") as f:
        data = json.load(f)
    return data["#eta"]["ptedges"]


@pytest.mark.parametrize("func", [
    lambda i: 1,
    lambda i: exp(-i / 20.),
])
@pytest.mark.parametrize("etype", [
    # "normal",
    "#pi^{0}",
])
def test_rebins_flat_data(edges, edges_eta, func, stop):
    hist = ROOT.TH1F("hist", "test", len(edges) - 1, array.array('d', edges))
    hist.label = "original"
    for i in br.hrange(hist):
        hist.SetBinContent(i, func(i))
        hist.SetBinError(i, func(i) * 1e-2)

    hist.logy = True
    with open_loggs() as loggs:
        rebinned = RebinTransformer(True, edges_eta).transform(hist, loggs)
        rebinned.label = "transformed"

    Comparator(stop=stop).compare(hist, rebinned)
    assert hist is not rebinned


@pytest.mark.skip()
@pytest.fixture
def pion_data(region):
    histname = "hPt_#pi^{0}_primary_standard"
    return DataVault().input("single #pi^{0}", region,
                             "PhysEff", histname=histname)


# @pytest.mark.skip()
@pytest.mark.onlylocal
@pytest.mark.parametrize("etype", [
    "#pi^{0}",
])
@pytest.mark.parametrize("region", [
    "low",
    "high",
])
def test_rebins_data(etype, edges, pion_data, stop):
    with open_loggs() as loggs:
        hist = SingleHistReader().transform(pion_data, loggs)
        hist.label = "original"
        hist.logy = True

        rebinned = RebinTransformer(False, edges).transform(hist, loggs)
        rebinned.label = "transformed"
        rebinned.logy = True
        Comparator(stop=stop).compare(hist, rebinned)
