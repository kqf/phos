#!/usr/bin/python


import ROOT
import json
from tests.general_test import TestImages, GeneralTest


class TestRatio(TestImages, GeneralTest):

    def save_config(self):
        conffile = 'config/test_ratio.json'
        rfile = 'input/testfile_ratio.root'
        histnames = ['data', 'mixing']
        pfile = 'results/test.pdf'
        data = {
            "histograms":
            {
                rfile + '/' + histname:
                {
                    "label": histname,
                    "color": 1001 + i,
                    "title":
                    "Testing ratio plots ;x - quantity; y - observable",
                    'ratio': i
                }
                for i, histname in enumerate(histnames)
            },
            "canvas":
            {
                "size": 5,
                "logy": 1,
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
            f = ROOT.TF1(
                'f%d' % i, 'TMath::Exp(- %0.2f * x) + (1 - %d) * TMath::Exp(-1 * (x - 9) * (x - 9))' % (i / 10., i), 0, 20)
            histogram = ROOT.TH1F(
                histname, "Testing %dth iteration ..." % i, 1000, 0, 20)
            histogram.FillRandom('f%d' % i, 100000)
            histogram.Write()
        ofile.Close()
