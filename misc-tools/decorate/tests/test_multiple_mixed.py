import os
import ROOT
import json
from tests.mc import fill_random
from drawtools.style import Styler
import pytest


@pytest.fixture
def config():
    conffile = 'config/test_multiple_mixed.json'
    filename = 'input/testfile_multiple_hists_mixed.root'
    histnames = [
        'hSomeHistInModule_%d',
        'hAnotherHistInTheModule_%d',
        'hYetAnotherHistInTheModule_%d']
    drawoptions = ['colz', '', 'same']

    # Draw two first histograms on the last one separate
    data = {
        "multiplot":
        {
            filename + '/' + histname:
            {
                "option": drawoptions[i],
                "priority": len(histnames) - i,
                "title": "Random distribution; #alpha; #beta",
                "separate": int(i == 0),
                "color": 1000 + i,
                "oname": 'results/' + histname.replace('%d', '.pdf')
            }
            for i, histname in enumerate(histnames)
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

    save_histogram(filename, histnames)
    yield conffile
    os.remove(conffile)
    os.remove(filename)


def save_histogram(filename, histnames):
    ofile = ROOT.TFile(filename, "update")

    def h1(sm):
        return ROOT.TH1F(
            histname % sm, "Testing ...", 200, 0, 10)

    def h2(sm):
        return ROOT.TH2F(
            histname %
            sm, "Testing ...", 20, 0, 100, 20, 0, 100)

    for s, histname in enumerate(histnames):
        for sm in range(1, 5):
            histogram = h1(sm) if s != 0 else h2(sm)
            fill_random(histogram, [s, sm])
            histogram.Write()
    ofile.Close()


def test_styles(config):
    style = Styler(config)
    style.draw()
