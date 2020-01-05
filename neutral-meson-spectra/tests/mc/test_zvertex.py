import pytest


from spectrum.pipeline import SingleHistReader
from spectrum.pipeline import ComparePipeline
from spectrum.output import open_loggs

from spectrum.vault import DataVault


@pytest.fixture
def data():
    return (
        DataVault().input("data", listname="Qual", histname="hZvertex"),
        DataVault().input("pythia8", listname="Qual", histname="hZvertex"),
    )


@pytest.mark.onlylocal
@pytest.mark.interactive
def test_compare_pipeline(data):
    pipeline = ComparePipeline([
        ("data", SingleHistReader()),
        ("pythia8", SingleHistReader()),
    ])

    with open_loggs("Z vertex") as loggs:
        pipeline.transform(data, loggs)
