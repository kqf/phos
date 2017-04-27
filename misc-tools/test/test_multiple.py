#!/usr/bin/python

import ROOT
import json
import random
from test.general_test import TestImages, GeneralTest

class TestMultipleImages(TestImages, GeneralTest):

	
	def save_config(self):
		conffile = 'config/test_single.json'
		rfile    = 'input/testfile_multiple_hists.root'
		histname = 'hSomeHistInModule_%d'
		pfile    = 'results/test_multiple_hists.pdf'

		data = {
					"multiplot": 
						{ 
							rfile + '/' + histname:
							{
								"option": "colz", 
								"title": "Random distribution; #alpha; #beta"
							}
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
			self.fill_random(histogram, None)
			histogram.Write()
		ofile.Close()

	def fill_random(self, histogram, pars):
		if type(histogram) is ROOT.TH1F:
			return self.fill_random1d(histogram, pars)

		self.fill_random2d(histogram, pars)

	def fill_random1d(self, histogram, pars):
		f1 = ROOT.TF1('mfunc', "TMath::Exp( -1 * (x - [0]) * (x - [0]) / [1] / [1] )")
		f1.SetParameter(0, 3 - pars[1])
		f1.SetParameter(1, 3 - pars[0])
		histogram.FillRandom('mfunc', 10000)


	def fill_random2d(self, histogram, pars):
		xaxis, yaxis = histogram.GetXaxis(), histogram.GetYaxis()
		iterate = lambda x: range(1, x.GetNbins() + 1)

		for i in iterate(xaxis):
			for j in iterate(yaxis):
				histogram.SetBinContent(i, j, random.randint(1, 5))

