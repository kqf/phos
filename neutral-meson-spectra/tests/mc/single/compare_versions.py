from spectrum.pipeline import ComparePipeline
from spectrum.efficiency import Efficiency
from spectrum.options import CompositeEfficiencyOptions, Options
from spectrum.options import CompositeOptions
from spectrum.analysis import Analysis
from spectrum.output import AnalysisOutput

from vault.datavault import DataVault


def define_datasets():
    datasets = [
        {
            DataVault().input("single #pi^{0} iteration d3 nonlin13",
                              "low",
                              listname="PhysEff" + i): (0, 7.0),
            DataVault().input("single #pi^{0} iteration d3 nonlin13",
                              "high",
                              listname="PhysEff" + i): (7.0, 20)
        }
        for i in ["3"]
    ]

    datasets = datasets + [
        {
            DataVault().input("single #pi^{0}",
                              "low",
                              listname="PhysEff" + i): (0, 7.0),
            DataVault().input("single #pi^{0}",
                              "high",
                              listname="PhysEff" + i): (7.0, 20)
        }
        for i in [""]
    ]

    reference = [
        {
            DataVault().input("single #pi^{0}",
                              "low",
                              listname="PhysEff",
                              ): (0, 7.0),
            DataVault().input("single #pi^{0}",
                              "high",
                              listname="PhysEff",
                              ): (7.0, 20)
        },
    ]
    datasets = datasets + reference
    names = "old", "new", "the oldest one"
    return names, datasets


def test_efficiencies():
    names, datasets = define_datasets()
    particle = "#pi^{0}"
    estimator = ComparePipeline([
        (name, Efficiency(CompositeEfficiencyOptions(
            uinput,
            particle,
        )))
        for name, uinput in zip(names, datasets)
    ], plot=True)

    estimator.transform(
        datasets,
        loggs=AnalysisOutput("compare different datasts")
    )


def test_yields():
    names, datasets = define_datasets()
    particle = "#pi^{0}"
    data = [('data', Analysis(Options()))]
    estimator = ComparePipeline(data + [
        (name,
         Analysis(CompositeOptions(uinput, particle)))
        for name, uinput in zip(names, datasets)
    ], True)

    estimator.transform(
        define_datasets(),
        "compare different datasts"
    )
