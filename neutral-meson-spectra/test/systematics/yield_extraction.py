import unittest
from spectrum.options import Options
from spectrum.comparator import Comparator

from spectrum.broot import BROOT as br
from spectrum.corrected_yield import CorrectedYield
from spectrum.options import CorrectedYieldOptions
from spectrum.options import CompositeCorrectedYieldOptions
from vault.datavault import DataVault

import ROOT


class YieldExtractioinUncertanity(object):

    def average_yiled(self, histos):
        average = histos[0].Clone(histos[0].GetName() + '_average')
        average.Reset()
        average.Sumw2()
        llist = ROOT.TList()

        for h in histos:
            llist.Add(h)

        average.Merge(llist)
        average.Scale(1. / len(histos))
        average.label = 'averaged yield'
        return average

    def transofrm(self, data, loggs):
        spectrums, options = [], Options()
        for frange, flab in zip([[0.06, 0.22], [0.04, 0.20], [0.08, 0.24]], ['low', 'mid', 'wide']):
            for bckgr in ['pol1', 'pol2']:
                for marker, par in enumerate(['CrystalBall', 'Gaus']):
                    for nsigmas in [2, 3]:
                        options.spectrum.dead = True
                        options.pt.label = 'n#sigma = {0} {1} {2} {3}'.format(
                            nsigmas, par, bckgr, flab)
                        options.spectrum.nsigmas = nsigmas
                        options.param.fitf = par
                        options.param.background = bckgr
                        options.param.fit_range = frange

                        copt = CorrectedYieldOptions()
                        copt.analysis = options
                        spectrum = CorrectedYield(copt).transform(data, loggs)
                        spectrum.marker = marker
                        spectrums.append(spectrum)

        diff = Comparator(stop=self.stop, oname='spectrum_extraction_methods')
        diff.compare(spectrums)

        average = self.average_yiled(spectrums)
        diff = Comparator(stop=self.stop, oname='yield_deviation_from_average')
        diff.compare_ratios(spectrums, average)

        uncert, rms, mean = br.systematic_deviation(spectrums)
        uncert.SetTitle(
            'Systematic uncertanity from yield extraction (RMS/mean)')
        diff = Comparator(stop=self.stop, oname='syst-error-yield-extraction')
        diff.compare(uncert)
        return self.outsys.histogram(spectrums[0], uncert)


class TestYieldExtractionUncertanity(unittest.TestCase):

    # @unittest.skip('')
    def test_yield_extraction_uncertanity_pion(self):
        # production = "single #pi^{0} iteration3 yield aliphysics"
        production = "single #pi^{0} iteration d3 nonlin14"
        unified_inputs = {
            DataVault().input(production, "low"): (0, 8.0),
            DataVault().input(production, "high"): (4.0, 20)
        }

        data = [
            DataVault().input("data"),
            unified_inputs
        ]

        estimator = CorrectedYield(
            CompositeCorrectedYieldOptions(
                particle="#pi^{0}",
                unified_inputs=unified_inputs
            )
        )
        estimator.transform(data, "corrected yield #pi^{0}")
