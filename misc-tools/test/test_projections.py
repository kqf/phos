#!/usr/bin/python

import ROOT
import json
import random
from test.general_test import TestImages, GeneralTest
import unittest

class TestProjections(TestImages, GeneralTest):

    def save_config(self):
        conffile = 'config/test_projection.json'
        rfile    = 'input/testfile_projections.root'
        histname = 'hSomeHistogram'
        pfile    = 'results/test_projections.pdf'

        data = {
                    "histograms": 
                        { 
                            rfile + '/' + histname: {"option": "colz", "title": "Trying projections; #alpha; #beta", "projectx": 50}
                        }, 
                    "canvas": 
                        {"size":  5, "logy":  0, "gridx": 0, "gridy": 0, "output": pfile} 
               }

        with open(conffile, 'w') as outfile:
            json.dump(data, outfile)
        return conffile, rfile, histname

    def save_histogram(self, filename, histname):
        ofile = ROOT.TFile(filename, "update")
        histogram = ROOT.TH2F(histname, "Testing projections ...", 200, 0, 100, 200, 0, 100)
        for i in range(1, histogram.GetXaxis().GetNbins() + 1):
            for j in range(1, histogram.GetXaxis().GetNbins() + 1):
                histogram.SetBinContent(i, j, i * i * j * random.randint(1, 4))

        histogram.Write()
        ofile.Close()