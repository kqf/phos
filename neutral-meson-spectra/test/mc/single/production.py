import unittest

from vault.datavault import DataVault
from spectrum.options import CompositeNonlinearityOptions
from spectrum.mc import Nonlinearity, Decalibration, Shape
from spectrum.output import AnalysisOutput


def inputs(production, is_nonlin=False):
    listname = "PhysEff"
    histname = "MassPt"
    if is_nonlin:
        listname = "PhysNonlin"
        histname = "MassPt_SM0"

    unified_inputs = {
        DataVault().input(production, "low",
                          listname=listname,
                          histname=histname): (0, 7),
        DataVault().input(production, "high",
                          listname=listname,
                          histname=histname): (7, 20)
    }
    return unified_inputs


class TestProductions(unittest.TestCase):

    def setUp(self):
        self.production_name = "single #pi^{0} iteration d3 nonlin"

    # @unittest.skip('')
    def test_nonlinearity(self):
        unified_inputs = inputs(self.production_name, is_nonlin=True)
        options = CompositeNonlinearityOptions(unified_inputs)
        options.fitf = None
        estimator = Nonlinearity(options)
        nonlinearity = estimator.transform(
            [
                DataVault().input("data", listname="PhysNonlinEst",
                                  histname="MassPt_SM0"),
                unified_inputs
            ],
            "nonlinearity estimation"
        )
        self.assertGreater(nonlinearity.GetEntries(), 0)

    @unittest.skip('')
    def test_decalibration(self):
        unified_inputs = inputs(self.production_name)
        options = CompositeNonlinearityOptions(unified_inputs)
        options.fitf = None
        estimator = Decalibration(options)
        nonlinearity = estimator.transform(
            [
                DataVault().input("data"),
                unified_inputs
            ],
            "nonlinearity estimation"
        )
        self.assertGreater(nonlinearity.GetEntries(), 0)

    def test_weights(self):
        unified_inputs = inputs(self.production_name)
        options = CompositeNonlinearityOptions(unified_inputs)
        options.fitf = None
        estimator = Shape(options)
        nonlinearity = estimator.transform(
            [
                DataVault().input("data"),
                unified_inputs
            ],
            "nonlinearity estimation"
        )
        self.assertGreater(nonlinearity.GetEntries(), 0)
