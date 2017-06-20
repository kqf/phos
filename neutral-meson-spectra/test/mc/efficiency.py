#!/usr/bin/python

from spectrum.spectrum import Spectrum
from spectrum.ptanalyzer import PtDependent
from spectrum.options import Options
from spectrum.input import Input, read_histogram
from spectrum.sutils import get_canvas, adjust_canvas
from spectrum.sutils import wait
from spectrum.comparator import Comparator
from spectrum.sutils import save_tobject

from test.analysis.test_check_different_modules import run_analysis

import ROOT

import os.path
import unittest


def cache(function):
    def cached(self, infile, genfile, label):
        res = function(self, infile, genfile, label)
        res.label = label
        return res
    return cached

class Efficiency(unittest.TestCase):


    def setUp(self):
        self.mc_selection = 'MCStudyOnlyTender'
        self.selection = 'PhysNonlinOnlyTender'
        self.file = 'input-data/Pythia-LHC16-iteration21.root'


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
    def efficiency(self, iname, genname, label):
        oname = iname + '.eff'
        ratio = self.readEfficiency(oname)
        if ratio: 
            return ratio

        f = lambda x, y, z: Spectrum(x, label=y, mode = 'q', options = z).evaluate()
        ## Calculate yield for mc 

        true = read_histogram(iname, self.mc_selection, genname, label = 'Generated', priority = 0)
        PtDependent.divide_bin_width(true)

        reco = f(Input(iname, self.selection).read(), 'Reconstructed', Options())[4]
        PtDependent.divide_bin_width(reco)

        reco.logy = True
        true.logy = True

        # data.fifunc = self.getNonlinearityFunction()

        # true.Scale(reco.Integral() / true.Integral())

        diff = Comparator()
        ratio = diff.compare(reco, true)

        if oname: save_tobject(ratio, oname)
        return ratio

    # @unittest.skip('')
    def testOutput(self):
        eff2 = self.efficiency('input-data/Pythia-LHC16-iteration21.root', 'hPtGeneratedMC_#pi^{0}', 'pythia')
        eff1 = self.efficiency('input-data/EPOS-LHC16-iteration3.root', 'hPtGeneratedMC_#pi^{0}', 'epos')

        diff = Comparator()
        diff.compare(eff1, eff2)


    # @unittest.skip('')
    def testEffDifferentModules(self):
        modules = run_analysis(Options(), self.file, 'PhysNonlinOnlyTender')
        c1 = get_canvas(1./2, 1.)
        diff = Comparator()
        diff.compare(modules)

        true = read_histogram(self.file, 'MCStudyOnlyTender', 'hPtGeneratedMC_#pi^{0}', label = 'Generated', priority = 0)
        PtDependent.divide_bin_width(true)

        spectrums = zip(*modules)[2]
        map(lambda x: x.SetTitle('Efficiency per module'), spectrums)
        map(lambda x: x.GetYaxis().SetTitle('measured / generated'), spectrums)
        map(PtDependent.divide_bin_width, spectrums)
        diff.compare_ratios(spectrums, true)


    def testDifferentContributions(self):
        read = lambda x, y, p = 1: read_histogram(self.file, self.mc_selection, x, label = y, priority = p)


        filename = 'hPtGeneratedMC_#pi^{0}'
        labels = 'secondary', '#pi^{-}', '#pi^{+}', '#eta', '#omega', 'K_0^s', '#Lambda'

        hists = map(lambda x: read(filename + '_' + x,  x, 999), labels)
        hists[0].logy = True

        map(PtDependent.divide_bin_width, hists)

        diff = Comparator()
        diff.compare(hists)

        pall = read(filename, 'all', -1)
        pall.logy = True

        pprimary = read(filename + '_primary', 'primary', 999)
        pprimary.logy = True

        map(PtDependent.divide_bin_width, (primary, pall))
        diff.compare(pall, primary)








