#!/usr/bin/python


import unittest
import ROOT
import json
import os
from drawtools.style import Styler


class TestSpectrum(unittest.TestCase):

	def setUp(self):
		# Different values in some pt-bins can be explained by limited statistics in those bins.
		#
		self.conffile = 'config/test_single.json'
		self.infile, histname = self.save_config(self.conffile)
		self.save_histogram(self.infile, histname)

	def save_config(self, filename):
		rfile    = 'input/testfile.root'
		histname = 'hHistogram'
		pfile    = 'results/test.pdf'
		data = {"histograms": { rfile + '/' + histname: {"label": "test 1", "color": 37, "title": "Test;x;y"} }, "canvas": {"size":  5, "logy":  1, "gridx": 1, "legend": [0.7, 0.7, 0.89, 0.88], "output": pfile} }
		with open(filename, 'w') as outfile:
			json.dump(data, outfile)
		return rfile, histname

	def save_histogram(self, filename, histname):
		ofile = ROOT.TFile(filename, "update")
		histogram = ROOT.TH1F(histname, "Testing ...", 1000, -3, 3)
		histogram.FillRandom('gaus', 100000)
		histogram.Write()
		ofile.Close()

	def testDrawing(self):
		style = Styler(self.conffile)
		style.draw()


	def tearDown(self):
		os.remove(self.conffile)
		os.remove(self.infile)


