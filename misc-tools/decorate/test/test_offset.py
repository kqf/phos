#!/usr/bin/python


import ROOT
import json
import unittest
import os
from drawtools.offset import Offset


class TestOffset(unittest.TestCase):

    def setUp(self):
        self.conffile, self.infile, histname = self.save_config()
        self.save_histogram(self.infile, histname)

    def save_config(self):
        conffile = 'config/test_offset.json'
        rfile = 'input/testfile_offset.root'
        histnames = ['data', 'mixing']
        pfile = 'results/test.pdf'
        data = {
            "histograms":
            {
                rfile + '/' + histname:
                {
                    "xofset": 1.5,
                    "xofset": 1.7,
                    "title":
                    "Testing offsets for ratio plots ;x; y - obs",
                    "label": histname,
                    "color": 1001 + i,
                    'ratio': i,
                    "ratiofit": 1,
                    "fitrange": [1, 14],
                    "fitfunc": '[0] * x + [1]',
                    "fitpars": [0, 0]
                }
                for i, histname in enumerate(histnames)
            },
            "canvas":
            {
                "size": 5,
                "logy": 0,
                "gridx": 1,
                "gridy": 1,
                "legend": [0.78, 0.7, 0.89, 0.88],
                "output": pfile
            }
        }

        with open(conffile, 'w') as outfile:
            json.dump(data, outfile)

        return conffile, rfile, histnames

    def save_histogram(self, filename, histnames):
        ofile = ROOT.TFile(filename, "update")
        for i, histname in enumerate(histnames):
            f = ROOT.TF1('f%d' % i, '-%0.2f * x + 20' % (i * 0.3 + 0.5), 0, 20)
            histogram = ROOT.TH1F(
                histname, "Testing %dth iteration ..." % i, 1000, 0, 20)
            histogram.FillRandom('f%d' % i, 100000)
            histogram.Write()
        ofile.Close()

    def testDrawing(self):
        offset = Offset(self.conffile)
        offset.draw()

    def tearDown(self):
        os.remove(self.conffile)
        os.remove(self.infile)