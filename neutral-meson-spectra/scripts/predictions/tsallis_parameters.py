import json
import pytest
import numpy as np
import pandas as pd

import spectrum.broot as br
import spectrum.sutils as su


@pytest.fixture
def pars():
    with open("config/predictions/tsallis-pion.json") as f:
        data = json.load(f)
    return pd.DataFrame(data.values())


def test_tsallis_parameter_dependence(pars):
    print(pars)
    graph = br.graph(
        "test",
        pars["energy"],
        pars["C"],
        np.zeros_like(pars["energy"]),
        pars["dC"])
    graph.SetMarkerColor(4)
    graph.SetMarkerStyle(21)

    with su.canvas():
        graph.Draw('ap')
