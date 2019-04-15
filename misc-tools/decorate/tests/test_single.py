import os
import ROOT
import json
import pytest
from drawtools.style import Styler


@pytest.fixture
def config():
    conffile = 'config/test_single.json'
    filename = 'input/testfile.root'
    histname = 'hHistogram'
    pfile = 'results/test.pdf'
    data = {
        "histograms":
        {
            filename + '/' + histname:
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

    save_histogram(filename, histname)
    yield conffile
    os.remove(filename)
    os.remove(conffile)


def save_histogram(filename, histname):
    ofile = ROOT.TFile(filename, "update")
    histogram = ROOT.TH1F(histname, "Testing ...", 1000, -3, 3)
    histogram.FillRandom('gaus', 100000)
    histogram.Write()
    ofile.Close()


def test_styles(config):
    Styler(config).draw()
