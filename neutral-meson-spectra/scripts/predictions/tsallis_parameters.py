import json
import pytest
import numpy as np
import pandas as pd
import ROOT
from array import array

import spectrum.sutils as su


@pytest.fixture
def pars():
    with open("config/predictions/tsallis-pion.json") as f:
        data = json.load(f)
    return pd.DataFrame(data.values())


def tgraph(x, y, ex, ey):
    print(y, ey)
    return ROOT.TGraphErrors(
        len(x),
        array('f', x),
        array('f', y),
        array('f', ex),
        array('f', ey)
    )


def test_tsallis_parameter_dependence(pars):
    print(pars)
    graph = tgraph(
        pars["energy"],
        pars["C"],
        np.zeros_like(pars["energy"]),
        pars["dC"])
    graph.SetMarkerColor(4)
    graph.SetMarkerStyle(21)

    with su.canvas():
        graph.Draw('ap')
