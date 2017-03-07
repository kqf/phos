#!/usr/bin/python


import ROOT
import json
from drawtools.style import Styler
from test.general_test import TestImages


class SingleImage(TestImages):

	def save_config(self):
		conffile = 'config/test_single.json'
		rfile    = 'input/testfile.root'
		histname = 'hHistogram'
		pfile    = 'results/test.pdf'
		data = {"histograms": { rfile + '/' + histname: {"label": "test 1", "color": 37, "title": "Test;x;y"} }, "canvas": {"size":  5, "logy":  1, "gridx": 1, "legend": [0.7, 0.7, 0.89, 0.88], "output": pfile} }
		with open(conffile, 'w') as outfile:
			json.dump(data, outfile)
		return conffile, rfile, histname

	def save_histogram(self, filename, histname):
		ofile = ROOT.TFile(filename, "update")
		histogram = ROOT.TH1F(histname, "Testing ...", 1000, -3, 3)
		histogram.FillRandom('gaus', 100000)
		histogram.Write()
		ofile.Close()

	def testDrawing(self):
		style = Styler(self.conffile)
		style.draw()
