#!/usr/bin/python

from spectrum.spectrum import Spectrum
from spectrum.options import Options
from spectrum.input import Input, read_histogram
from spectrum.sutils import get_canvas, adjust_canvas
from spectrum.comparator import Comparator
from test.analysis.test_check_different_modules import run_analysis

from spectrum.broot import BROOT as br

import ROOT

import os.path
import unittest


class Efficiency(object):

    def __init__(self, genname, label, iname):
        super(Efficiency, self).__init__()
        self.selection = 'MCStudyOnlyTender'
        self.iname = iname
        self.genname = genname
        self.label = label
        self.oname = 'input-data/efficiency-{0}-{1}.root'.format(self.iname, label)

    def eff(self):
        try:
            return self.read_efficiency()
        except IOError:
            return self.efficiency()


    def read_efficiency(self):
        if not os.path.isfile(self.oname):
            raise IOError('No such file: {0}'.format(self.oname))

        infile = ROOT.TFile(self.oname)
        result = infile.GetListOfKeys().At(0).ReadObj()
        result.label = self.label
        return result


    def true(self, label = 'Generated'):
        true = read_histogram(self.iname, self.selection, self.genname, label = label, priority = 0)
        print true
        true.logy = True
        return br.scalew(true)


    def reco(self):
        inp = Input(self.iname, self.selection, 'MassPt')
        reco = Spectrum(inp, Options(self.label, mode = 'q')).evaluate().npi0
        reco.logy = True
        return br.scalew(reco)


    def efficiency(self):
        reco, true = self.reco(), self.true()

        diff = Comparator()
        ratio = diff.compare(reco, true)
        ratio.label = self.label

        if self.oname: 
            br.io.save(ratio, self.oname)
        return ratio

class CalculateEfficiency(unittest.TestCase):


    def setUp(self):
        self.selection = 'PhysNonlinOnlyTender'
        # self.pythiaf = 'input-data/scaled-LHC17f8a.root'
        self.pythiaf = 'input-data/Pythia-LHC16-a5.root'
        self.eposf = 'input-data/scaled-LHC17f8a.root'

        # To compare more than 1 production
        # self.productions = {'pythia': 'input-data/Pythia-LHC16-a5.root'}
        self.productions = {'pythia': 'Pythia-LHC16-a5', 'jet jet': 'scaled-LHC17f8a'}
        # self.eposf = 'input-data/EPOS-LHC16-iteration3.root'

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
        diff = Comparator()
        diff.compare(efficiencies)


    @unittest.skip('')
    def testSpectrums(self):
        """ 
            This test checks the denominators of the efficiencies.
        """
        true = [Efficiency(self.true_pt_mc, k, f).true(k) for k, f in self.productions.iteritems()]
        map(lambda x: x.Scale(1./ x.Integral('w')), true)

        diff = Comparator(size = (0.5, 1))
        diff.compare(true)


    @unittest.skip('')
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

        spectrums = zip(*modules).npi0
        map(lambda x: x.SetTitle('Efficiency per module'), spectrums)
        map(lambda x: x.GetYaxis().SetTitle('measured / generated'), spectrums)
        map(br.scalew, spectrums)

        true = Efficiency(self.true_pt_mc, '', self.pythiaf).true()
        diff.compare_ratios(spectrums, true)


