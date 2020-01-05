import pytest

from spectrum.analysis import Analysis
from spectrum.options import Options
from spectrum.vault import AnalysisInput
from spectrum.comparator import Comparator
from spectrum.output import open_loggs

import spectrum.broot as br
from tests.playground.phspace import InclusiveGenerator
from spectrum.vault import DataVault


@pytest.fixture
def data():
    return DataVault().file("data")


@pytest.fixture
def data_spmc():
    return DataVault().file("single #pi^{0}", "low")


@pytest.mark.skip("")
@pytest.mark.onlylocal
def test_recreates_the_same_shape(data):
    gen_file_name = "LHC16-fake.root"
    generator = InclusiveGenerator(
        data,
        "config/test_algorithm.json",
        gen_file_name=gen_file_name,
        flat=True
    )

    generated = generator.generate(1000)
    with open_loggs("reconstructing generated spectra") as loggs:
        reconstructed = Analysis(Options()).transform(
            AnalysisInput(gen_file_name, generator.selname), loggs
        )
    Comparator.compare(
        map(br.scalew, [reconstructed, generated])
    )


@pytest.mark.skip("")
@pytest.mark.onlylocal
def test_generate_mc(data_spmc):
    generator = InclusiveGenerator(
        data_spmc,
        "config/test_algorithm.json",
        selname="PhysEff",
        gen_file_name="LHC16-single.root",
        flat=True
    )
    generator.generate(1000)
