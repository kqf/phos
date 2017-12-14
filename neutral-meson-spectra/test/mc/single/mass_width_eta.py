#!/usr/bin/python

from spectrum.spectrum import Spectrum, CompositeSpectrum
from spectrum.input import Input
from spectrum.options import Options
from spectrum.broot import BROOT as br
import spectrum.comparator as cmpr

import unittest
import operator


class TestMassWidth(unittest.TestCase):

    def setUp(self):
        ddir = '/single/nonlin1/'
        files = {
                    ddir + 'LHC17j3c1': (0, 10),
                    ddir + 'LHC17j3c2': (4, 20)
                }

        inputs = [Input(f, 'PhysEffOnlyTender') for f in files]
        inputs = map(operator.methodcaller('read'), inputs)

        options = [Options.spmc(rr, particle='eta') for f, rr in files.iteritems()]
        f = lambda x, y: Spectrum(x, y).evaluate()
        self.results = map(f, inputs, options)



    def test_different_mc_productions(self):
        masses, widths = zip(*self.results)[0:2]

        indata, doptions = Input('uncorrected/LHC16', 'EtaTender'), Options('data', particle='eta')
        dmass, dwidth = Spectrum(indata, doptions).evaluate()[0:2]

        diff = cmpr.Comparator((0.5, 1.), rrange = (0, 2),
                        # crange=(0.4, 0.5), 
                        oname = 'compared-spmc-masses')
        diff.compare(list(masses) + [dmass])

        diff = cmpr.Comparator((0.5, 1.), rrange = (0, 2),
                        crange=(0.0, 0.02), oname = 'compared-spmc-widths')
        diff.compare(list(widths) + [dwidth])


    @unittest.skip('')
    def test_spectrum_shape(self):
        datadir = '/single/weight2/'
        inputs = {
            Input(datadir + 'LHC17j3b1', 'PhysEffOnlyTender'): (0, 7), 
            Input(datadir + 'LHC17j3b2', 'PhysEffOnlyTender'): (7, 20)
        }

        spectrum_estimator = CompositeSpectrum(inputs)
        spmc = spectrum_estimator.evaluate()
        br.scalew(spmc.spectrum, 1. / spmc.spectrum.Integral())
        spmc.spectrum.label = 'mc'

        dinp, dopt = Input('LHC16', 'PhysOnlyTender'), Options('data', 'd')
        data = Spectrum(dinp, dopt).evaluate()
        br.scalew(data.spectrum, 1. / data.spectrum.Integral())

        diff = cmpr.Comparator()
        diff.compare(data.spectrum, spmc.spectrum)


