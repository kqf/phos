import unittest

from spectrum.efficiency import Efficiency, EfficiencyMultirange
from spectrum.comparator import Comparator
from spectrum.broot import BROOT as br
from vault.datavault import DataVault
from spectrum.input import Input
from spectrum.output import AnalysisOutput
from spectrum.options import EfficiencyOptions, MultirangeEfficiencyOptions

def check_particle(particle="#pi^{0}"):

    inputs = Input(
        DataVault().file("single {}".format(particle), "high"), 
        "PhysEff"
    )
    options = EfficiencyOptions()


    edges = [6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0, 10.5, 11.0, 11.5, 12.0, 12.5, 13.0, 13.5, 14.0, 14.5, 15.0, 15.5, 16.0, 16.5, 17.0, 17.5, 18.0, 18.5, 19.0, 19.5, 20.0]
    # edges = [6.0, 6.1, 6.199999999999999, 6.299999999999999, 6.399999999999999, 6.499999999999998, 6.599999999999998, 6.6999999999999975, 6.799999999999997, 6.899999999999997, 6.9999999999999964, 7.099999999999996, 7.199999999999996, 7.299999999999995, 7.399999999999995, 7.499999999999995, 7.599999999999994, 7.699999999999994, 7.799999999999994, 7.899999999999993, 7.999999999999993, 8.099999999999993, 8.199999999999992, 8.299999999999992, 8.399999999999991, 8.499999999999991, 8.59999999999999, 8.69999999999999, 8.79999999999999, 8.89999999999999]
    # edges = [6.0, 6.2, 6.4, 6.6000000000000005, 6.800000000000001, 7.000000000000001, 7.200000000000001, 7.400000000000001, 7.600000000000001, 7.800000000000002, 8.000000000000002, 8.200000000000003, 8.400000000000002, 8.600000000000001, 8.800000000000002, 9.000000000000004, 9.200000000000003, 9.400000000000002, 9.600000000000003, 9.800000000000004, 10.000000000000004, 10.200000000000003, 10.400000000000004, 10.600000000000005, 10.800000000000004, 11.000000000000004, 11.200000000000005, 11.400000000000006, 11.600000000000005, 11.800000000000004]
    rebins = [0] * (len(edges) - 1)
    options.analysis.pt.ptedges = edges
    options.analysis.pt.rebins = rebins
    options.analysis.invmass.use_mixed = False

    loggs = AnalysisOutput("test_high_momentum_{}".format(particle), "#eta")

    estimator = Efficiency(options)
    efficiency = estimator.transform(inputs, loggs)
    efficiency.SetTitle('Efficiency at high p_{T}')

    diff = Comparator()
    diff.compare(efficiency)    

    loggs.plot(False)


class TestHighMomentum(unittest.TestCase):

    def test_pi0(self):
    	check_particle("#pi^{0}")

    def test_eta(self):
    	check_particle("#eta")
