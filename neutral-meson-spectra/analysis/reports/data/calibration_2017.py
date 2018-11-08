import unittest
from spectrum.analysis import Analysis
from spectrum.pipeline import TransformerBase
from spectrum.pipeline import Pipeline
from spectrum.pipeline import HistogramSelector
from spectrum.options import Options
from spectrum.comparator import Comparator
from spectrum.output import AnalysisOutput

from vault.datavault import DataVault


class MassAnalysis(TransformerBase):
    def __init__(self, options, plot=False):
        super(MassAnalysis, self).__init__(plot)
        self.pipeline = Pipeline([
            ("analysis", Analysis(options)),
            ("mass", HistogramSelector("mass")),
        ])


class TestDifferentPeriods(unittest.TestCase):
    def test_different_calibrations(self):
        periods = "egijklmor"
        options = Options(ptrange="config/pt-periods.json")
        masses = [
            MassAnalysis(options).transform(
                DataVault("debug-ledger.json").input("LHC17 qa1", "LHC17" + p),
                {}
            )
            for p in periods
        ]
        mass_2016 = MassAnalysis(options).transform(
            DataVault().input("data"),
            {}
        )
        loggs = AnalysisOutput("calibration lhc17")
        for mass, p in zip(masses, periods):
            diff = Comparator(labels=("LHC17" + p, "LHC16"))
            local_loggs = {}
            diff.compare(mass, mass_2016, loggs=local_loggs)
            loggs["LHC17" + p] = local_loggs
        loggs.plot()
