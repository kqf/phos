from spectrum.analysis import Analysis
from spectrum.pipeline import TransformerBase
from spectrum.pipeline import ComparePipeline, Pipeline
from spectrum.pipeline import HistogramSelector, HistogramScaler
from spectrum.pipeline import FunctionTransformer
from spectrum.vault import DataVault


def tof_data():
    return (
        DataVault().input(
            "data",
            "staging tof",
            listname="TagAndProbleTOF",
            histname="MassEnergyTOF_SM0"
        ),
        DataVault().input(
            "data",
            "staging tof",
            listname="TagAndProbleTOF",
            histname="MassEnergyAll_SM0"
        ),
    )


def tof_data_old():
    return (
        DataVault().input(
            "data",
            "uncorrected",
            listname="TagAndProbleTOFOnlyTender",
            histname="MassEnergyTOF_SM0"),
        DataVault().input(
            "data",
            "uncorrected",
            listname="TagAndProbleTOFOnlyTender",
            histname="MassEnergyAll_SM0"
        ),
    )


class TagAndProbe(TransformerBase):
    def __init__(self, options, plot=False):
        super(TagAndProbe, self).__init__(plot)
        compare = ComparePipeline([
            ("tof cut",
                Pipeline([
                    ("analysis", Analysis(options.analysis, plot)),
                    ("nmesons", HistogramSelector("nmesons")),
                    ('scale', HistogramScaler())
                ])
             ),
            ("no cut",
                Pipeline([
                    ("analysis", Analysis(options.analysis, plot)),
                    ("nmesons", HistogramSelector("nmesons")),
                    ('scale', HistogramScaler())
                ])
             ),
        ], plot, ratio="B")

        def rename(x, loggs):
            x.SetTitle(options.title)
            return x

        self.pipeline = Pipeline([
            ("compare", compare),
            ("rename", FunctionTransformer(rename)),
        ])
