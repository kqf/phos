from spectrum.spectrum import Spectrum
from spectrum.input import Input, TimecutInput, read_histogram
from spectrum.sutils import get_canvas, adjust_canvas
from spectrum.options import Options
from spectrum.comparator import Visualizer, Comparator
from spectrum.sutils import save_tobject, scalew

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
        for bckgr in ['pol1', 'pol2']:
            for marker, par in enumerate(['CrystalBall', 'Gaus']):
                for nsigmas in [2, 3]:
                    options.spectrum.dead = True
                    options.pt.label = 'n#sigma = {0} {1} {2}'.format(nsigmas, par, bckgr)
                    options.spectrum.nsigmas = nsigmas
                    options.param.fitf = par
                    options.param.background = bckgr

                    spectrum = self.spectrum(options)
                    spectrum.marker = marker
                    spectrums.append(spectrum)


        diff = Comparator(oname = 'spectrum_extraction_methods')
        diff.compare(spectrums)

        average = self.average_yiled(spectrums)
        diff = Comparator(oname = 'yield_deviation_from_average')
        diff.compare_ratios(spectrums, average)

        # TODO: How to get uncertanity from this

  



    def spectrum(self, options):
        inp = Input(self.infile, self.selection)
        spectrum = Spectrum(inp, options).evaluate().spectrum
        return scalew(spectrum)  





