import unittest

from spectrum.efficiency import Efficiency
from spectrum.comparator import Comparator
from spectrum.broot import BROOT as br
from test.mc.single.efficiency import FitEfficiency
from vault.datavault import DataVault


class TestEfficiencyPi0(unittest.TestCase):

    def test_eff_overlap(self):
        files = {
            DataVault().file("single #pi^{0}", "low"): (0, 5),
            DataVault().file("single #pi^{0}", "high"): (9, 20)
        }

        estimator = FitEfficiency("#pi^{0}", None)
        estimator.estimate(files)