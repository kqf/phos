import pytest
import json

import spectrum.broot as br
from spectrum.spectra import energies, DataExtractor
from spectrum.pipeline import FunctionTransformer
from spectrum.pipeline import DataFitter, Pipeline


def fitted(fitf):
    def p(x, loggs):
        return x

    def fit_results(x, loggs):
        res = br.fit_results(x.fitf)
        res["energy"] = x.energy
        return res

    return Pipeline([
        ("cyield", DataExtractor()),
        ("fit", DataFitter(fitf)),
        ("show", FunctionTransformer(p)),
        ("res", FunctionTransformer(fit_results)),
    ])


@pytest.fixture
def rawdata(particle, tcm):
    return energies(particle, fitted(tcm))


@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    "#eta",
])
def test_downloads_from_hepdata(particle, stop, rawdata, ltitle):
    with open("config/predictions/tcm.json") as f:
        final = json.load(f)
    final[particle] = rawdata
    with open("config/predictions/tcm.json", "w") as f:
        json.dump(final, f, indent=4)
