import unittest
import pytest

from spectrum.output import AnalysisOutput
from uncertainties.tof import TofUncertainty, TofUncertaintyOptions
from vault.datavault import DataVault

# from spectrum.comparator import Comparator


class TestTofUncertainty(unittest.TestCase):

    def test(self):
        tof = TofUncertainty(TofUncertaintyOptions())
        output = tof.transform(
            (
                DataVault().input("data"),
                DataVault().input("data"),
            ),
            loggs=AnalysisOutput("test the composite analysis")
        )
        # for o in output:
        #     Comparator().compare(o)
        self.assertGreater(len(output), 0)
