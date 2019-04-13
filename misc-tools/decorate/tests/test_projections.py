import ROOT
import json
import pytest
import random
from drawtools.style import Styler


@pytest.fixture
def config():
    conffile = 'config/test_projection.json'
    filename = 'input/testfile_projections.root'
    histname = 'hSomeHistogram'
    pfile = 'results/test_projections.pdf'

    data = {
        "histograms":
        {
            filename + '/' + histname:
            {
                "title": "Trying projections; #alpha; #beta",
                "option": "colz",
                "projectx": 50
            }
        },
        "canvas":
        {
            "size": 5,
            "logy": 0,
            "gridx": 0,
            "gridy": 0,
            "output": pfile
        }
    }

    save_histogram(filename, histname)
    with open(conffile, 'w') as outfile:
        json.dump(data, outfile)
    yield conffile


def save_histogram(filename, histname):
    ofile = ROOT.TFile(filename, "update")
    histogram = ROOT.TH2F(
        histname, "Testing projections ...", 200, 0, 100, 200, 0, 100)
    for i in range(1, histogram.GetXaxis().GetNbins() + 1):
        for j in range(1, histogram.GetXaxis().GetNbins() + 1):
            histogram.SetBinContent(i, j, i * i * j * random.randint(1, 4))

    histogram.Write()
    ofile.Close()


def test_styles(config):
    Styler(config).draw()
