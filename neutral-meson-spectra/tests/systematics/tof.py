import unittest
import pytest

from spectrum.output import AnalysisOutput
from uncertainties.tof import TofUncertainty, TofUncertaintyOptions
from vault.datavault import DataVault

# from spectrum.comparator import Comparator


class TestTofUncertainty(unittest.TestCase):

    @pytest.mark.onlylocal
    def test(self):
        tof = TofUncertainty(TofUncertaintyOptions())
        loggs = AnalysisOutput("tof uncertainty")
        output = tof.transform(
            (
                DataVault().input("data"),
                DataVault().input("data", "isolated", histname="MassPtSM0"),
            ),
            loggs=loggs
        )
        loggs.plot()
        # Comparator().compare(output)
        self.assertGreater(len(output), 0)
