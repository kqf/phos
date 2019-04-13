import os
import ROOT
import json
import pytest
from drawtools.style import Styler


@pytest.fixture
def config():
    conffile = 'config/test_ratio.json'
    filename = 'input/testfile_ratio.root'
    histnames = ['data', 'mixing']
    pfile = 'results/test.pdf'
    data = {
        "histograms":
        {
            filename + '/' + histname:
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

    save_histogram(filename, histnames)
    yield conffile
    os.remove(conffile)
    os.remove(filename)


def save_histogram(filename, histnames):
    ofile = ROOT.TFile(filename, "update")
    for i, histname in enumerate(histnames):
        func = ROOT.TF1('f%d' % i, """
            TMath::Exp(- %0.2f * x) +
            (1 - %d) * TMath::Exp(-1 * (x - 9) * (x - 9))
            """ % (i / 10., i), 0, 20)
        histogram = ROOT.TH1F(
            histname, "Testing %dth iteration ..." % i, 1000, 0, 20)
        histogram.FillRandom('f%d' % i, 100000)
        histogram.Write()
        del func
    ofile.Close()


def test_styles(config):
    Styler(config).draw()
