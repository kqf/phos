import unittest
from spectrum.analysis import Analysis
from spectrum.pipeline import TransformerBase
from spectrum.pipeline import Pipeline
from spectrum.pipeline import HistogramSelector
from spectrum.options import Options
from spectrum.comparator import Comparator
from spectrum.output import AnalysisOutput

from vault.datavault import DataVault


class CalibrationAnalysis(TransformerBase):
    def __init__(self, atype, options, plot=False):
        super(CalibrationAnalysis, self).__init__(plot)
        self.pipeline = Pipeline([
            ("analysis", Analysis(options)),
            (atype, HistogramSelector(atype)),
        ])


class TestDifferentPeriods(unittest.TestCase):
    def test_different_calibrations_mass(self):
        self.calibration("mass")

    def test_different_calibrations_width(self):
        self.calibration("width")

    def calibration(self, atype):
        periods = "egijklmor"
        options = Options(ptrange="config/pt-periods.json")
        masses = [
            CalibrationAnalysis(atype, options).transform(
                DataVault("debug-ledger.json").input("LHC17 qa1", "LHC17" + p),
                {}
            )
            for p in periods
        ]
        mass_2016 = CalibrationAnalysis(atype, options).transform(
            DataVault().input("data"),
            {}
        )
        loggs = AnalysisOutput("calibration lhc17 {}".format(atype))
        for mass, p in zip(masses, periods):
            diff = Comparator(labels=("LHC17" + p, "LHC16"))
            local_loggs = {}
            diff.compare(mass, mass_2016, loggs=local_loggs)
            loggs["LHC17" + p] = local_loggs
        loggs.plot()
