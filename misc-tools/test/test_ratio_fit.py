#!/usr/bin/python


import ROOT
import json
from test.general_test import TestImages, GeneralTest


class TestFitRatio(TestImages, GeneralTest):

    def save_config(self):
        conffile = 'config/test_ratio_fit.json'
        rfile = 'input/testfile_ratio_fit.root'
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
            # f = ROOT.TF1('f%d' % i, '- %0.2f * x' % ((i + 1) / 10., i + 1.), 0, 20)
            f = ROOT.TF1('f%d' % i, '-%0.2f * x + 20' % (i * 0.3 + 0.5), 0, 20)
            histogram = ROOT.TH1F(
                histname, "Testing %dth iteration ..." % i, 1000, 0, 20)
            histogram.FillRandom('f%d' % i, 100000)
            histogram.Write()
        ofile.Close()
