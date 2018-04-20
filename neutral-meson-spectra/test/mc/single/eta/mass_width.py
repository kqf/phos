#!/usr/bin/python

from spectrum.spectrum import Spectrum
from spectrum.input import Input
from spectrum.options import Options

from test.mc.single.mass_width import TestMassWidth
from vault.datavault import DataVault


class TestMassWidthEta(TestMassWidth):

    def setUp(self):
        files = {
            DataVault().file("single #eta", "low"): (0, 10),
            DataVault().file("single #eta", "high"): (4, 20)
        }

        inputs = [Input(f, 'PhysEffOnlyTender') for f in files]
        # inputs = map(operator.methodcaller('read'), inputs)

        options = [Options.spmc(rr, particle='eta')
                   for f, rr in files.iteritems()]

        def f(x, y):
            return Spectrum(x, y).evaluate()

        self.results = map(f, inputs, options)

        self.shape_inputs = {inp: frange for inp,
                             frange in zip(inputs, files.values())}
