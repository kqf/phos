import unittest
import pytest

from spectrum.analysis import Analysis
from spectrum.options import Options
from spectrum.input import Input

from spectrum.broot import BROOT as br
from tests.playground.phspace import InclusiveGenerator

import test.check_default


class CheckAlgorithm(test.check_default.CheckDefault):
    def setUp(self):
        super(CheckAlgorithm, self).setUp()
        self.clean = False

    @unittest.skip('')
    def test_recreates_the_same_shape(self):
        genfilename = 'LHC16-fake.root'
        infile, conf = ('input-data/data/LHC16.root',
                        'config/test_algorithm.json')
        generator = InclusiveGenerator(
            infile,
            conf,
            genfilename=genfilename,
            flat=True
        )

        generated = generator.generate(1000)
        generated.logy = 1
        generated.priority = 1
        reconstructed = Analysis(Options()).transform(
            Input(genfilename, generator.selname), {}
        )
        self.results = map(br.scalew, [reconstructed, generated])
        # os.remove(genfilename)


@pytest.mark.onlylocal
def test_generate_mc(self):
    genfilename = 'LHC16-single.root'
    infile, conf = (
        'input-data/mc/single/pi0/nonlin/LHC17j3b1.root',
        'config/test_algorithm.json'
    )
    generator = InclusiveGenerator(
        infile,
        conf,
        selname='PhysEff',
        genfilename=genfilename,
        flat=True
    )
    generator.generate(10000)
