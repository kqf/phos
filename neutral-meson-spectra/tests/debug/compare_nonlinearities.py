import unittest

from spectrum.analysis import Analysis
from spectrum.options import CompositeNonlinearityOptions
from spectrum.output import AnalysisOutput
from spectrum.pipeline import ComparePipeline
from spectrum.pipeline import HistogramSelector
from spectrum.pipeline import Pipeline
from tools.mc import Nonlinearity
from vault.datavault import DataVault


def define_datasets():
    histname = "MassPt"
    listname = "Phys"
    mclistname = "PhysEff"
    productions = [
        "single #pi^{0}",
        "single #pi^{0} debug7",
        "single #pi^{0} scan nonlinearity",
    ]

    datasets = [
        {
            DataVault().input(production,
                              "low",
                              listname=mclistname,
                              histname=histname): (0, 8.0),
            DataVault().input(production,
                              "high",
                              listname=mclistname,
                              histname=histname): (4.0, 20)
        }
        for production in productions
    ]

    data = DataVault().input("data", listname=listname, histname=histname)
    options = list(map(CompositeNonlinearityOptions, datasets))
    mcinput = [[data, i] for i in datasets]
    names = "p-p 13 TeV", "p-p 5.02 TeV", "p-Pb 5.02 TeV"
    return names, options, mcinput


def test_nonlinearity():
    names, options, datasets = define_datasets()
    estimator = ComparePipeline([
        (name, Nonlinearity(opt, False))
        for name, opt in zip(names, options)
    ], plot=True)

    loggs = AnalysisOutput("compare nonlinearities")
    estimator.transform(datasets, loggs)
    loggs.plot()


@unittest.skip('')
def test_masses():
    def mass(options):
        return Pipeline([
            ("", Analysis(options)),
            ("", HistogramSelector("mass"))
        ])

    names, options, datasets = define_datasets()
    _, datasets = zip(*datasets)
    estimator = ComparePipeline([
        (name, mass(opt.mc))
        for name, opt in zip(names, options)
    ], plot=True)

    loggs = AnalysisOutput("compare masses")
    estimator.transform(datasets, loggs)
    loggs.plot()
