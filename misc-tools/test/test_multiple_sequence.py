#!/usr/bin/python

import ROOT
import json
from test.test_multiple import TestImages, GeneralTest

# TODO: Use double inheritance to avoid double running
class TestMultipleSequential(TestImages, GeneralTest):

	def save_config(self):
		conffile = 'config/test_multiple_sequential.json'
		rfile    = 'input/testfile_multiple_hists.root'
		histnames = ['hSomeHistInModule_%d', 'hAnotherHistInTheModule_%d', 'hYetAnotherHistInTheModule_%d']
		pfile    = 'results/test_multiple_hists.pdf'

		data = {
					"multiplot": 
					{ 
						rfile + '/' + histname:
						{
							"option": "colz",
							"title": "Random distribution; #alpha; #beta",
							"separate": 1,
							"oname": 'results/' + histname.replace('%d', '.pdf')
						}
						for histname in histnames
					},

					"canvas": 
					{
						"size":  5,
						"logy":  0, 
						"gridx": 0
					} 
		   }

		with open(conffile, 'w') as outfile:
			json.dump(data, outfile)
		return conffile, rfile, histnames

	def save_histogram(self, filename, histnames):
		ofile = ROOT.TFile(filename, "update")
		for s, histname in enumerate(histnames):
			for sm in range(1, 5):
				histogram = ROOT.TH2F(histname % sm, "Testing ...", 20 * (s + 1), 0, 100, 20 * (s + 1), 0, 100)
				self.fill_random(histogram, None)
				histogram.Write()
		ofile.Close()