#!/usr/bin/python

import ROOT
import json
from test.general_test import TestImages, GeneralTest


class TestDifferentModules(TestImages, GeneralTest):
    """
            Test multiple onedimensional histogramsi in different modules
    """

    def save_config(self):
        conffile = 'config/test_different_modules.json'
        rfile = 'input/testfile_multiple_modules.root'
        histname = 'hHistInModule_%d'
        pfile = 'results/test_multiple_modules.pdf'
        suff = '_run_%d'
        nruns = 3
        data = {
            "multiplot":
            {
                rfile + '/' + histname + suff % i:
                {

                    "title": "Random distribution; variable; counts",
                    "label": "run %d" % i,
                    "color": 1000 + i,
                    "option": "same" * int(i != 0)
                }

                for i in range(nruns)
            },
            "canvas":
            {"size": 5, "logy": 0, "gridy": 1, "gridx": 1, "output": pfile}
        }

        with open(conffile, 'w') as outfile:
            json.dump(data, outfile)

        return conffile, rfile, [histname, suff, nruns]

    def save_histogram(self, filename, histnames):
        histname, suff, nruns = histnames
        ofile = ROOT.TFile(filename, "update")
        f1 = ROOT.TF1(
            'mfunc', "TMath::Exp( -1 * (x - [0]) * (x - [0]) / [1] / [1] )")

        for i in range(1, 5):
            for r in range(nruns):
                histogram = ROOT.TH1F(
                    histname % i + suff % r,
                    "Testing histogram, dummy name ...", 200, -3, 3)
                f1.SetParameter(0, nruns - i)
                f1.SetParameter(1, nruns - r)
                histogram.FillRandom('mfunc', 10000)
                histogram.Write()
        ofile.Close()
