import pytest


from spectrum.input import SingleHistInput
from spectrum.pipeline import ComparePipeline
from spectrum.output import open_loggs

from vault.datavault import DataVault


@pytest.fixture
def data():
    return (
        DataVault().input("data", listname="Qual", label="data"),
        DataVault().input("pythia8", listname="Qual", label="pythia8"),
    )


@pytest.mark.onlylocal
@pytest.mark.interactive
def test_compare_pipeline(data):
    pipeline = ComparePipeline([
        (dataset.label, SingleHistInput("hZvertex"))
        for dataset in data
    ])

    with open_loggs("Z vertex") as loggs:
        pipeline.transform(data, loggs)
