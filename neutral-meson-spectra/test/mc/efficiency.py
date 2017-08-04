#!/usr/bin/python

from spectrum.spectrum import Spectrum
from spectrum.options import Options
from spectrum.input import Input, read_histogram
from spectrum.sutils import get_canvas, adjust_canvas
from spectrum.sutils import wait, scalew
from spectrum.comparator import Comparator
from spectrum.sutils import save_tobject

from test.analysis.test_check_different_modules import run_analysis

import ROOT

import os.path
import unittest


# TODO: Delete this ugly chunk of code
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
        # self.pythiaf = 'input-data/scaled-LHC17f8a.root'
        self.pythiaf = 'input-data/Pythia-LHC16-a5.root'
        self.eposf = 'input-data/scaled-LHC17f8a.root'

        # To compare more than 1 production
        # self.productions = {'pythia': 'input-data/Pythia-LHC16-a5.root'}
        self.productions = {'pythia': 'input-data/Pythia-LHC16-a5.root', 'jet jet': 'input-data/scaled-LHC17f8a.root'}
        # self.eposf = 'input-data/EPOS-LHC16-iteration3.root'
        self.true_pt_mc = 'hPt_#pi^{0}'


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

    def get_true_distribution(self, iname, genname, label = 'Generated'):
        true = read_histogram(iname, self.mc_selection, genname, label = label, priority = 0)
        scalew(true)
        true.logy = True
        return true



    def reco(self, iname, label):
        f = lambda x, y, z: Spectrum(x, label=y, mode = 'q', options = z).evaluate()
        reco = f(Input(iname, self.selection, 'MassPt').read(), label, Options())[4]
        reco.logy = True
        return scalew(reco)

    @cache
    def efficiency(self, iname, genname, label):
        oname = '{0}.{1}.eff'.format(iname, label)
        ratio = self.readEfficiency(oname)
        if ratio: 
            return ratio

        reco = self.reco(iname, label)
        true = self.get_true_distribution(iname, genname, 'Generated')

        diff = Comparator()
        ratio = diff.compare(reco, true)
        ratio.label = label

        if oname: save_tobject(ratio, oname)
        return ratio

    @unittest.skip('')
    def testProductions(self):
        efficiencies = [self.efficiency(f, self.true_pt_mc + '_primary_', k) for k, f in self.productions.iteritems()]
        diff = Comparator()
        diff.compare(efficiencies)


    def testSpectrums(self):
        """ 
            This test checks the denominators of the efficiencies.
        """
        true = [self.get_true_distribution(f, self.true_pt_mc + '_primary_', k) for k, f in self.productions.iteritems()]
        map(lambda x: x.Scale(1./ x.Integral('w')), true)
        diff = Comparator((0.5, 1))
        diff.compare(true)


    @unittest.skip('')
    def testRecoSpectrums(self):
        reco = [self.reco(f, k) for k, f in self.productions.iteritems()]
        map(lambda x: x.Scale(1./ x.Integral('w')), reco)
        diff = Comparator()
        diff.compare(reco)


    @unittest.skip('')
    def testEffDifferentModules(self):
        modules = run_analysis(Options(), self.pythiaf, self.selection)
        c1 = get_canvas(1./2, 1.)
        diff = Comparator()
        diff.compare(modules)

        true = read_histogram(self.pythiaf, self.mc_selection, self.true_pt_mc, label = 'Generated', priority = 0)
        scalew(true)

        spectrums = zip(*modules)[2]
        map(lambda x: x.SetTitle('Efficiency per module'), spectrums)
        map(lambda x: x.GetYaxis().SetTitle('measured / generated'), spectrums)
        map(scalew, spectrums)
        diff.compare_ratios(spectrums, true)


    @unittest.skip('')
    def testPrimaryEfficiency(self):
        primary = self.efficiency(self.pythiaf, self.true_pt_mc + '_primary_', 'primaries')
        total = self.efficiency(self.pythiaf, self.true_pt_mc, 'total')

        diff = Comparator()
        diff.compare(primary, total)

