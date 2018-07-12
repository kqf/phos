import unittest

from vault.datavault import DataVault
from spectrum.options import CompositeNonlinearityOptions
from spectrum.mc import Nonlinearity, Decalibration, Shape
from spectrum.output import AnalysisOutput


def inputs(production, is_nonlin=False):
    listname = "PhysEff"
    histname = "MassPt"

    unified_inputs = {
        DataVault().input(production, "low",
                          listname=listname,
                          histname=histname): (0.0, 8.0),
        DataVault().input(production, "high",
                          listname=listname,
                          histname=histname): (4.0, 20.0)
    }
    return unified_inputs


class TestProductionsPi0(unittest.TestCase):

    def setUp(self):
        self.production_name = "single #pi^{0} debug2"
        self.particle = "#pi^{0}"
        # self.production_name = "single #eta nonlin"
        # self.particle = "#eta"

    # @unittest.skip('')
    def test_nonlinearity(self):
        unified_inputs = inputs(self.production_name, is_nonlin=True)
        options = CompositeNonlinearityOptions(
            unified_inputs,
            self.particle,
        )
        options.fitf = None
        estimator = Nonlinearity(options)
        nonlinearity = estimator.transform(
            [
                DataVault().input("data", listname="Phys",
                                  histname="MassPt"),
                unified_inputs
            ],
            "nonlinearity estimation {}".format(self.particle)
        )
        self.assertGreater(nonlinearity.GetEntries(), 0)

    @unittest.skip('')
    def test_decalibration(self):
        unified_inputs = inputs(self.production_name)
        options = CompositeNonlinearityOptions(
            unified_inputs,
            self.particle,)
        options.fitf = None
        estimator = Decalibration(options, plot=True)
        loggs = AnalysisOutput(
            "decalibration estimation {}".format(self.particle))
        nonlinearity = estimator.transform(
            [
                DataVault().input("data"),
                unified_inputs
            ],
            loggs
        )
        loggs.plot()
        self.assertGreater(nonlinearity.GetEntries(), 0)

    @unittest.skip('')
    def test_weights(self):
        unified_inputs = inputs(self.production_name)
        options = CompositeNonlinearityOptions(
            unified_inputs,
            particle=self.particle
        )
        options.fitf = None
        estimator = Shape(options)
        nonlinearity = estimator.transform(
            [
                DataVault().input("data"),
                unified_inputs
            ],
            loggs=AnalysisOutput("weight estimation")
        )
        self.assertGreater(nonlinearity.GetEntries(), 0)
