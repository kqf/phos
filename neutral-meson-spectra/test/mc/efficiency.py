#!/usr/bin/python

import unittest
from spectrum.efficiency import Efficiency

from spectrum.options import Options
from spectrum.comparator import Comparator
from test.analysis.test_check_different_modules import run_analysis
from spectrum.broot import BROOT as br



# NB: This test is to compare different efficiencies 
#     estimated from different productions
#

class CalculateEfficiency(unittest.TestCase):


    def setUp(self):
        self.selection = 'PhysNonlinOnlyTender'
        # self.pythiaf = 'input-data/scaled-LHC17f8a.root'
        self.pythiaf = 'input-data/LHC17d20a.root'
        self.jetjetf = 'input-data/pythia-jet-jet.root'


        # To compare more than 1 production
        # self.productions = {'pythia': 'input-data/Pythia-LHC16-a5.root'}
        self.productions = {'pythia': 'Pythia-LHC16-a5', 'jet jet': 'pythia-jet-jet'}
        self.true_pt_mc = 'hPt_#pi^{0}_primary_'


    def getEffitiencyFunction(self):
        pass

    @unittest.skip('Modify it later')
    def testFitEfficiencyFunction(self):
        # Calculate and fit efficiency
        pass


    # @unittest.skip('')
    def testProductions(self):
        """
            Calculate and compare efficiencies for different productions
        """
        efficiencies = [Efficiency(self.true_pt_mc, *p).eff() for p in self.productions.iteritems()]

        diff = Comparator(oname='different-efficiencies')
        diff.compare(efficiencies)


    # @unittest.skip('')
    def testSpectrums(self):
        """ 
            This test checks the denominators of the efficiencies.
        """
        true = [Efficiency(self.true_pt_mc, k, f).true(k) for k, f in self.productions.iteritems()]
        map(lambda x: x.Scale(1./ x.Integral('w')), true)

        diff = Comparator(size = (0.5, 1))
        diff.compare(true)


    # @unittest.skip('')
    def testRecoSpectrums(self):
        """ 
            This test checks the Numerators of the efficiencies.
        """
        reco = [Efficiency(self.true_pt_mc, *p).reco() for p in self.productions.iteritems()]
        map(lambda x: x.Scale(1./ x.Integral('w')), reco)
        diff = Comparator()
        diff.compare(reco)


    # @unittest.skip('')
    def testEffDifferentModules(self):
        opt = Options(mode='d')
        opt.pt.config = 'config/test_different_modules.json'
        modules = run_analysis(opt, self.pythiaf, self.selection)
        diff = Comparator()
        diff.compare(modules)

        spectrums = [sm.npi0 for sm in modules]
        map(lambda x: x.SetTitle('Efficiency per module'), spectrums)
        map(lambda x: x.GetYaxis().SetTitle('measured / generated'), spectrums)
        map(br.scalew, spectrums)

        true = Efficiency(self.true_pt_mc, '', self.pythiaf).true()
        diff.compare_ratios(spectrums, true)


