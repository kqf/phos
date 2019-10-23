import pytest
import pandas as pd
import spectrum.broot as br
from spectrum.plotter import plot


@pytest.mark.parametrize("par", ["A", "n", "C"])
def test_tsallis_parameters(par):
    df = pd.read_json("config/predictions/tsallis-pion.json").T
    df = df.sort_values(by=["energy"])
    parameter = br.graph(par, df["energy"], df[par], dy=df["d{}".format(par)])
    style = {
        "logy": False,
        "logx": False,
    }
    plot([parameter], **style)
