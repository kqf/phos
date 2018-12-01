import pytest


from spectrum.input import SingleHistInput
from spectrum.pipeline import ComparePipeline

from vault.datavault import DataVault


@pytest.mark.onlylocal
@pytest.mark.interactive
def test_compare_pipeline():
    # TODO: Add Qual selection to the
    data = (
        DataVault().input("data", listname="Qual", label="data"),
        # DataVault().input("pythia8", listname="Qual", label="pythia8"),
    )
    pipeline = ComparePipeline([
        (dataset.label, SingleHistInput("hZvertex"))
        for dataset in data])
    pipeline.transform(data, {})
