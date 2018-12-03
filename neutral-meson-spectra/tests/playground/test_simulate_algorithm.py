import unittest
import pytest

from spectrum.analysis import Analysis
from spectrum.options import Options
from spectrum.input import Input
from spectrum.comparator import Comparator

from spectrum.broot import BROOT as br
from tests.playground.phspace import InclusiveGenerator


@unittest.skip('')
def test_recreates_the_same_shape():
    genfilename = 'LHC16-fake.root'
    infile = 'input-data/data/LHC16.root'
    generator = InclusiveGenerator(
        infile,
        'config/test_algorithm.json',
        genfilename=genfilename,
        flat=True
    )

    generated = generator.generate(1000)
    generated.priority = 1
    generated.logy = 1
    reconstructed = Analysis(Options()).transform(
        Input(genfilename, generator.selname), {}
    )
    Comparator.compare(
        map(br.scalew, [reconstructed, generated])
    )


@pytest.mark.onlylocal
def test_generate_mc():
    genfilename = 'LHC16-single.root'
    infile = 'input-data/mc/single/pi0/nonlin/LHC17j3b1.root'
    generator = InclusiveGenerator(
        infile,
        'config/test_algorithm.json',
        selname='PhysEff',
        genfilename=genfilename,
        flat=True
    )
    generator.generate(10000)
