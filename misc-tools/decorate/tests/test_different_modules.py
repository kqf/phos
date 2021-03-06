import os
import pytest
import ROOT
import json
from drawtools.style import Styler


@pytest.fixture
def config():
    conffile = 'config/test_different_modules.json'
    filename = 'input/testfile_multiple_modules.root'
    histname = 'hHistInModule_%d'
    pfile = 'results/test_multiple_modules.pdf'
    suff = '_run_%d'
    nruns = 3
    data = {
        "multiplot":
        {
            filename + '/' + histname + suff % i:
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

    ofile = ROOT.TFile(filename, "recreate")
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

    yield conffile
    os.remove(conffile)
    os.remove(filename)


def test_styles(config):
    style = Styler(config)
    style.draw()
