#!/usr/bin/python

import os

import test.check_default
from spectrum.input import Input
from spectrum.spectrum import Spectrum


# This way we can test different ways of counting the amount
# of particles in the given pt-range


def analytic_integral(mass, intgr_ranges):
    fitfun, background = mass.extract_data()
    a, b = intgr_ranges if intgr_ranges else mass.peak_function.fit_range
    return fitfun.Integral(a, b), fitfun.IntegralError(a, b)


def manual_counting(mass, intgr_ranges):
    a, b = intgr_ranges if intgr_ranges else mass.peak_function.fit_range
    area = sum(mass.signal.GetBinContent(i)
               for i in range(1, mass.signal.GetNbinsX() + 1)
               if (mass.signal.GetBinCenter(i) > a and
                   mass.signal.GetBinCenter(i) < b)
               )
    return area, area ** 0.5


class CheckAlgorithm(test.check_default.CheckDefault):
    def test(self):
        def inp():
            return Input('input-data/LHC16.root', 'PhysTender').read()

        original = Spectrum(inp(), 'testsignal', self.mode)

        naive = Spectrum(inp(), 'naive', self.mode)
        naive.analyzer.number_of_mesons = manual_counting

        analytic = Spectrum(inp(), 'analytic', self.mode)
        analytic.analyzer.number_of_mesons = analytic_integral

        self.results = map(lambda x: x.evaluate(), [naive, analytic, original])
