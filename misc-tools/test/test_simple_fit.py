#!/usr/bin/python


import ROOT
import json
from drawtools.style import Styler
from test.general_test import TestImages


class SimpleFit(TestImages):

	def save_config(self):
		conffile = 'config/test_simple_fit.json'
		rfile    = 'input/testfile_fit.root'
		histname = 'hHistogram'
		pfile    = 'results/test_fit.pdf'
		self.range = [1, 10]
		self.func  = "[0] * sin ([1] * x) / x + [2]"
		self.pars = [1., 3.14, 1.]
		data = { 
					"histograms": 
						{ rfile + '/' + histname: 
							{"label": "test fit", "color": 37, "title": "Test fitting; x;y",
							 "fitrange": self.range, "fitfunc": self.func, "fitpars": self.pars}
						},
					"canvas": 
						{"size":  5, "logy":  1, "gridx": 1, "legend": [0.7, 0.7, 0.89, 0.88], "output": pfile} 
				}

		with open(conffile, 'w') as outfile:
			json.dump(data, outfile)
		return conffile, rfile, histname

	def save_histogram(self, filename, histname):
		ofile = ROOT.TFile(filename, "update")
		histogram = ROOT.TH1F(histname, "Testing ...", 1000, -3, 3)
		function = ROOT.TF1('htest', self.func, *self.range)
		function.SetParameters(*self.pars)

		histogram.FillRandom('htest', 100000)
		histogram.Write()
		ofile.Close()

	def testDrawing(self):
		style = Styler(self.conffile)
		style.draw()
