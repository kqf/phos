import os
import ROOT
import json
import pytest
from drawtools.style import Styler
from tests.mc import fill_random


@pytest.fixture
def config():
    conffile = 'config/test_multiple_sequential.json'
    rfile = 'input/testfile_multiple_hists.root'
    histnames = [
        'hSomeHistInModule_%d',
        'hAnotherHistInTheModule_%d',
        'hYetAnotherHistInTheModule_%d'
    ]

    data = {
        "multiplot":
        {
            rfile + '/' + histname:
            {
                "option": "colz",
                "title": "Random distribution; #alpha; #beta",
                "separate": 1,
                "oname": 'results/' + histname.replace('%d', '.pdf')
            }
            for histname in histnames
        },

        "canvas":
        {
            "size": 5,
            "logy": 0,
            "gridx": 0
        }
    }

    with open(conffile, 'w') as outfile:
        json.dump(data, outfile)
    save_histogram(rfile, histnames)

    yield conffile
    os.remove(conffile)
    os.remove(rfile)


def save_histogram(filename, histnames):
    ofile = ROOT.TFile(filename, "update")
    for s, histname in enumerate(histnames):
        for sm in range(1, 5):
            histogram = ROOT.TH2F(
                histname % sm,
                "Testing ...",
                20 * (s + 1),
                0, 100, 20 * (s + 1), 0, 100)
            fill_random(histogram, None)
            histogram.Write()
    ofile.Close()


def test_styles(config):
    Styler(config).draw()
