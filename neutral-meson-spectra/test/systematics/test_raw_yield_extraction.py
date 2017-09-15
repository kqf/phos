from spectrum.spectrum import Spectrum
from spectrum.input import Input
from spectrum.options import Options
from spectrum.comparator import Comparator

from spectrum.broot import BROOT as br

import ROOT

import os.path
import unittest


class RawYieldSystematicError(unittest.TestCase):

    def setUp(self):
        # This should be studied on corrected yield
        #
        self.infile = 'LHC16'
        self.selection = 'PhysOnlyTender'


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


    def testRawYieldSysError(self):
        spectrums, options = [], Options('', mode = 'd')
        for frange, flab in zip([[0.06,0.22],[0.04,0.20],[0.08,0.24]], ['low', 'mid', 'wide']):
            for bckgr in ['pol1', 'pol2']:
                for marker, par in enumerate(['CrystalBall', 'Gaus']):
                    for nsigmas in [2, 3]:
                        options.spectrum.dead = True
                        options.pt.label = 'n#sigma = {0} {1} {2} {3}'.format(nsigmas, par, bckgr, flab)
                        options.spectrum.nsigmas = nsigmas
                        options.param.fitf = par
                        options.param.background = bckgr
                        options.param.fit_range = frange

                        spectrum = self.spectrum(options)
                        spectrum.marker = marker
                        spectrums.append(spectrum)


        diff = Comparator(oname = 'spectrum_extraction_methods')
        diff.compare(spectrums)

        average = self.average_yiled(spectrums)
        diff = Comparator(oname = 'yield_deviation_from_average')
        diff.compare_ratios(spectrums, average)

        uncert, rms, mean = br.systematic_deviation(spectrums)
        uncert.SetTitle('Systematic uncertanity from yield extraction (RMS/mean)')
        diff = Comparator(oname = 'syst-error-yield-extraction')
        diff.compare(uncert)


  



    def spectrum(self, options):
        inp = Input(self.infile, self.selection)
        spectrum = Spectrum(inp, options).evaluate().spectrum
        return br.scalew(spectrum)  





