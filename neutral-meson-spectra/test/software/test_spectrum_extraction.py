
import unittest
import ROOT
import sys
import json
import hashlib

from spectrum.spectrum import PtAnalyzer
from spectrum.spectrum import Spectrum
from spectrum.options import Options
from spectrum.input import Input


class TestSpectrum(unittest.TestCase):


	def setUp(self):
		# Different values in some pt-bins can be explained by limited statistics in those bins.
		#

		# Important:
		# This one should be set explicitely otherwise the test will fail
		# Because this global variable is set to Minuit2 in other tests
		ROOT.TVirtualFitter.SetDefaultFitter('Minuit')
		
		# NB: test Spectrum class, not Pt-dependent as it produces negative values due to wide integration range
		# Expected values for $\pi^0$ extraction

		with open('config/test_spectrum_extraction.json') as f:
			conf = json.load(f)

		self.infile = conf['infile']
		hsum = conf['hsum256']

		system = conf[sys.platform]
		self.nominal_pi0 = system['pi0']
		self.nominal_eta = system['eta']
		# Make sure that you have the same copy of LHC16.root file. 
		# sha 256 sum: 
		assert self.checkInputFile(hsum), "You are using a wrong file to test your data. Your hash sums don't coincide."
		self.longMessage = True


	def checkInputFile(self, hsum):
		hashsum = hashlib.sha256()
		with open(self.infile, 'rb') as f:
				data = f.read()
		hashsum.update(data)
		return hashsum.hexdigest() == hsum



	def testPi0SpectrumLHC16(self):
		second = Spectrum(Input(self.infile, 'PhysTender').read(), label = 'testsignal', mode = 'q').evaluate()
		actual = [ [ h.GetBinContent(i) for i in range(1, h.GetNbinsX())] for h in second]

		mymsg = '\n\nActual values:\n' + str(actual)
		for a, b, c in zip(self.nominal_pi0, actual, second):
			print 'Checking ', c.GetName()
			for aa, bb in zip(a, b): self.assertAlmostEqual(aa, bb, msg=mymsg)

	def testEtaSpectrumLHC16(self):
		indata = Input(self.infile, 'EtaTender')
		analysis = Spectrum(indata.read(), 'testsignal', 'q', options = Options(particle='eta'))
		histograms = analysis.evaluate()
		
		actual = [[h.GetBinContent(i) for i in range(1, h.GetNbinsX())] for h in histograms]
		mymsg = '\n\nActual values:\n' + str(actual)

		for a, b, c in zip(self.nominal_eta, actual, histograms):
			print 'Checking ', c.GetName()
			for aa, bb in zip(a, b): self.assertAlmostEqual(aa, bb, msg=mymsg)

