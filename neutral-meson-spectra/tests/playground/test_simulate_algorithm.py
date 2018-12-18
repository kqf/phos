import pytest

from spectrum.analysis import Analysis
from spectrum.options import Options
from spectrum.input import Input
from spectrum.comparator import Comparator

from spectrum.broot import BROOT as br
from tests.playground.phspace import InclusiveGenerator
from vault.datavault import DataVault


@pytest.mark.skip("")
@pytest.mark.onlylocal
def test_recreates_the_same_shape():
    gen_file_name = "LHC16-fake.root"
    generator = InclusiveGenerator(
        DataVault().file("data"),
        "config/test_algorithm.json",
        gen_file_name=gen_file_name,
        flat=True
    )

    generated = generator.generate(1000)
    generated.priority = 1
    generated.logy = 1
    reconstructed = Analysis(Options()).transform(
        Input(gen_file_name, generator.selname), {}
    )
    Comparator.compare(
        map(br.scalew, [reconstructed, generated])
    )


@pytest.mark.skip("")
@pytest.mark.onlylocal
def test_generate_mc():
    generator = InclusiveGenerator(
        DataVault().file("single #pi^{0}", "low"),
        "config/test_algorithm.json",
        selname="PhysEff",
        gen_file_name="LHC16-single.root",
        flat=True
    )
    generator.generate(1000)
