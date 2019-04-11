#!/usr/bin/python


import ROOT
import json
from tests.general_test import TestImages, GeneralTest


class SingleImage(TestImages, GeneralTest):

    def save_config(self):
        conffile = 'config/test_single.json'
        rfile = 'input/testfile.root'
        histname = 'hHistogram'
        pfile = 'results/test.pdf'
        data = {
            "histograms":
            {
                rfile + '/' + histname:
                {
                    "label": "test 1",
                    "color": 37,
                    "title": "Test;x;y",
                    "yprecision": "/ %.2f MeV"
                }
            },
            "canvas":
            {
                "size": 5,
                "logy": 1,
                "gridy": 1,
                "gridx": 1,
                "legend": [0.7, 0.7, 0.89, 0.88],
                "output": pfile
            }
        }

        with open(conffile, 'w') as outfile:
            json.dump(data, outfile)
        return conffile, rfile, histname

    def save_histogram(self, filename, histname):
        ofile = ROOT.TFile(filename, "update")
        histogram = ROOT.TH1F(histname, "Testing ...", 1000, -3, 3)
        histogram.FillRandom('gaus', 100000)
        histogram.Write()
        ofile.Close()
