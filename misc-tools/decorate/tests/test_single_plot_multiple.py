#!/usr/bin/python


import ROOT
import json
from tests.general_test import TestImages, GeneralTest


class SingleImageMultiplePlots(TestImages, GeneralTest):

    def save_config(self):
        conffile = 'config/test_single_multiple.json'
        filename = 'input/testfile_singlemultiple.root'
        histnames = ['hFirst', 'hSecond', 'hThird', 'hFourth']
        pfile = 'results/test.pdf'
        data = {
            "histograms":
            {
                filename + '/' + histname:
                {
                    "label": "plot %d" % i,
                    "color": 1000 + i,
                    "title": "Testing same plots ;x - quantity; y - observable"
                }
                for i, histname in enumerate(histnames)
            },
            "canvas":
            {
                "size": 5,
                "logy": 1,
                "gridx": 1,
                "gridy": 1, "legend": [0.78, 0.7, 0.89, 0.88],
                "output": pfile
            }
        }

        with open(conffile, 'w') as outfile:
            json.dump(data, outfile)

        return conffile, filename, histnames

    def save_histogram(self, filename, histnames):
        ofile = ROOT.TFile(filename, "update")
        for i, histname in enumerate(histnames):
            f = ROOT.TF1('f%d' % i, 'TMath::Exp(- %0.2f * x)' % (i / 10.), 0, 20)
            histogram = ROOT.TH1F(
                histname, "Testing %dth iteration ..." % i, 1000, 0, 20)
            histogram.FillRandom('f%d' % i, 100000)
            histogram.Write()
        ofile.Close()
