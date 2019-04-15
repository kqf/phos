import os
import ROOT
import json
import pytest
from drawtools.style import Styler


@pytest.fixture
def config():
    conffile = 'config/test_simple_fit.json'
    filename = 'input/testfile_fit.root'
    histname = 'hHistogram'
    pfile = 'results/test_fit.pdf'
    rrange = [1, 10]
    func = "[0] * sin ([1] * x) / x + [2]"
    pars = [1., 3.14, 1.]
    data = {
        "histograms":
        {
            filename + '/' + histname:
            {
                "title": "Test fitting; x, GeV; y",
                "label": "test data",
                "yprecision": " counts per %s GeV",
                "stats": "e",
                "color": 37,
                "fit": "",
                "fitrange": rrange,
                "fitfunc": func,
                "fitpars": pars
            }
        },
        "canvas":
        {
            "size": 5,
            "logy": 1,
            "gridx": 1,
            "gridy": 1,
            "legend": [0.14, 0.7, 0.34, 0.88],
            "output": pfile
        }
    }

    with open(conffile, 'w') as outfile:
        json.dump(data, outfile)

    save_histogram(filename, histname, pars, func, rrange)

    yield conffile
    os.remove(conffile)
    os.remove(filename)


def save_histogram(filename, histname, pars, func, rrange):
    ofile = ROOT.TFile(filename, "update")
    histogram = ROOT.TH1F(histname, "Testing ...", 1000, -3, 3)
    function = ROOT.TF1('htest', func, *rrange)
    function.SetParameters(*pars)
    histogram.FillRandom('htest', 100000)
    histogram.Write()
    ofile.Close()


def test_styles(config):
    Styler(config).draw()
