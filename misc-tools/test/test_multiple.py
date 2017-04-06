#!/usr/bin/python

import ROOT
import json
import random
from test.general_test import TestImages
from drawtools.style import Styler

class TestMultipleImages(TestImages):

	def save_config(self):
		conffile = 'config/test_single.json'
		rfile    = 'input/testfile_multiple_hists.root'
		histname = 'hSomeHistInModule_%d'
		pfile    = 'results/test_multiple_hists.pdf'

		data = {
					"hitmap": 
						{ 
							rfile + '/' + histname: {"option": "colz", "title": "Random distribution; #alpha; #beta"}
						}, 
					"canvas": 
						{"size":  5, "logy":  0, "gridx": 0, "output": pfile} 
			   }

		with open(conffile, 'w') as outfile:
			json.dump(data, outfile)
		return conffile, rfile, histname

	def save_histogram(self, filename, histname):
		ofile = ROOT.TFile(filename, "update")
		for i in range(1, 5):
			histogram = ROOT.TH2F(histname % i, "Testing ...", 20 * i, 0, 100, 20 * i, 0, 100)
			for i in range(1, histogram.GetXaxis().GetNbins() + 1):
				for j in range(1, histogram.GetXaxis().GetNbins() + 1):
					histogram.SetBinContent(i, j, random.randint(1, 5))
			histogram.Write()
		ofile.Close()

	def testDrawing(self):
		style = Styler(self.conffile)
		style.drawmap()