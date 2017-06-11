#!/usr/bin/python

from spectrum.spectrum import Spectrum
from spectrum.ptanalyzer import PtDependent
from spectrum.options import Options
from spectrum.input import Input, read_histogram
from spectrum.sutils import get_canvas, adjust_canvas
from spectrum.sutils import wait
from spectrum.comparator import Comparator
from spectrum.sutils import save_tobject

import ROOT

import os.path
import unittest


def cache(function):
    def cached(self, infile, label):
        res = function(self, infile, label)
        res.label = label
        return res
    return cached

class Efficiency(unittest.TestCase):


    def getEffitiencyFunction(self):
        pass

    @unittest.skip('Modify it later')
    def testFitEfficiencyFunction(self):
        c1 = adjust_canvas(get_canvas(1., resize = True))
        fname = 'datamcratio.root'
        ratio = self.readRatio(fname) if os.path.isfile(fname) else self.getRatio(fname)
        function = self.getNonlinearityFunction()
        ratio.SetAxisRange(0.90, 1.04, 'Y')
        ratio.Fit(function)
        ratio.Draw()
        wait(ratio.GetName())


    def readEfficiency(self, fname):
        infile = ROOT.TFile(fname)
        if not infile.IsOpen():
            return None
        return infile.GetListOfKeys().At(0).ReadObj()


    @cache
    def efficiency(self, iname, label):
        oname = iname + '.eff'
        ratio = self.readEfficiency(oname)
        if ratio: 
            return ratio

        f = lambda x, y, z: Spectrum(x, label=y, mode = 'q', options = z).evaluate()
        ## Calculate yield for mc 
        true = read_histogram(iname, 'MCStudyOnlyTender', 'hPtGeneratedMC_pi0', label = 'Generated', priority = 0)
        PtDependent.divide_bin_width(true)
        reco = f(Input(iname, 'PhysNonlinOnlyTender').read(), 'Reconstructed', Options())[4]
        PtDependent.divide_bin_width(reco)
        reco.logy = True
        true.logy = True

        # data.fifunc = self.getNonlinearityFunction()

        true.Scale(reco.Integral() / true.Integral())

        diff = Comparator()
        ratio = diff.compare(reco, true)

        if oname: save_tobject(ratio, oname)
        return ratio

    def testOutput(self):
        eff1 = self.efficiency('input-data/EPOS-LHC16-iteration3.root', 'epos')
        eff2 = self.efficiency('input-data/Pythia-LHC16-iteration17.root', 'pythia')

        
        diff = Comparator()
        diff.compare(eff1, eff2)


