import unittest
from spectrum.pipeline import ComparePipeline
from spectrum.options import CompositeNonlinearityOptions
from spectrum.output import AnalysisOutput
from tools.mc import Nonlinearity

from vault.datavault import DataVault


def define_datasets():
    histname = "MassPt"
    listname = "Phys"
    mclistname = "PhysEff"
    production = "single #pi^{0} iteration d3 nonlin12"

    # histname = "MassPt_SM0"
    # listname = "PhysNonlinEst"
    # mclistname = "PhysNonlin"
    datasets = []
    datasets = datasets + [
        {
            DataVault().input(production,
                              "low",
                              listname=mclistname + i,
                              histname=histname): (0, 7.0),
            DataVault().input(production,
                              "high",
                              listname=mclistname + i,
                              histname=histname): (7.0, 20)
        }
        for i in ["", "1", "2", "3"]
    ]

    data = DataVault().input("data", listname=listname, histname=histname)
    options = list(map(CompositeNonlinearityOptions, datasets))
    mcinput = [[data, i] for i in datasets]
    # names = "p", "p1", "p2", "p3", "n1", "n2", "n3", "initial param"
    names = "gamma", "pi0", "0.5 pi0", "2 pi0"
    return names, options, mcinput


class TestNonlinearities(unittest.TestCase):

    def test_nonlinearity(self):
        names, options, datasets = define_datasets()
        estimator = ComparePipeline([
            (name, Nonlinearity(opt, False))
            for name, opt in zip(names, options)
        ], plot=True)

        loggs = AnalysisOutput("nonlinearity estimation")
        estimator.transform(datasets, loggs)
