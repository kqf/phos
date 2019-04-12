import os
import ROOT
import json
import pytest
from drawtools.style import Styler
from tests.mc import fill_random


@pytest.fixture
def config():
    conffile = 'config/test_single.json'
    rfile = 'input/testfile_multiple_hists.root'
    histname = 'hSomeHistInModule_%d/'
    pfile = 'results/test_multiple_hists.pdf'

    data = {
        "multiplot":
        {
            rfile + '/' + histname:
            {
                "option": "colz",
                "title": "Random distribution; #alpha; #beta"
            }
        },
        "canvas":
        {
            "size": 5,
            "logy": 0,
            "gridx": 0,
            "output": pfile
        }
    }

    with open(conffile, 'w') as outfile:
        json.dump(data, outfile)

    ofile = ROOT.TFile(rfile, "update")
    for i in range(1, 5):
        histogram = ROOT.TH2F(
            histname % i, "Testing ...", 20 * i, 0, 100, 20 * i, 0, 100)
        fill_random(histogram, None)
        histogram.Write()
    ofile.Close()

    yield conffile
    os.remove(conffile)
    os.remove(rfile)


@pytest.mark.skip("Don't use multihist plots")
def test_styles(config):
    style = Styler(config)
    style.draw()
