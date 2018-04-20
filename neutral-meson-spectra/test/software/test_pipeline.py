import unittest
from spectrum.pipeline import ComparePipeline
from spectrum.input import SingleHistInput

from vault.datavault import DataVault
class TestPipeline(unittest.TestCase):

    def test_comparator(self):
        estimator = ComparePipeline([
            ('normal', SingleHistInput("hPt_#pi^{0}_primary_")),
            ('normal', SingleHistInput("hPt_#pi^{0}_primary_standard")),
        ])

        estimator.transform(
            [DataVault().input("single #pi^{0}", "low")] * 2,
            "Testing the compare pipeline"
        )
