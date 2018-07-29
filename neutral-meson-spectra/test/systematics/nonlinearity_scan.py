import ROOT
import unittest
from collections import OrderedDict

from spectrum.comparator import Comparator
from spectrum.options import CompositeNonlinearityScanOptions
from spectrum.options import CompositeNonlinearityOptions
from spectrum.output import AnalysisOutput
from tools.mc import Nonlinearity
from tools.scan import NonlinearityScan, form_histnames
from vault.datavault import DataVault


class ScanNonlinearities(unittest.TestCase):

    def setUp(self):
        self.nbins = 9

    @unittest.skip('')
    def test(self):
        prod = "single #pi^{0} scan nonlinearity"
        histnames = form_histnames(self.nbins)
        low = DataVault().input(prod, "low", inputs=histnames)
        high = DataVault().input(prod, "high", inputs=histnames)

        unified_inputs = OrderedDict([
            (low, (0.0, 8.0)),
            (high, (4.0, 20.0)),
        ])
        options = CompositeNonlinearityScanOptions(
            unified_inputs, nbins=self.nbins)
        options.factor = 1.

        low, high = low.read_multiple(2), high.read_multiple(2)
        mc_data = [(l, h) for l, h in zip(low, high)]

        chi2ndf = NonlinearityScan(options).transform(
            [DataVault().input("data"), mc_data],
            loggs=AnalysisOutput("testing the scan interface")
        )
        # TODO: Add this to the output
        ofile = ROOT.TFile("nonlinearity_scan.root", "recreate")
        chi2ndf.Write()
        ofile.Close()
        Comparator().compare(chi2ndf)

    # @unittest.skip('')
    def test_draw_most_optimal_nonlinearity(self):
        production = "single #pi^{0} scan nonlinearity5"
        minimum_index = 70
        minimum_index *= 2
        histname = form_histnames(self.nbins)[minimum_index]
        histname = histname[1:]  # Remove first h
        print histname
        # production = "single #pi^{0} iteration d3 nonlin14"
        # histname = "MassPt"
        unified_inputs = {
            DataVault().input(production, "low",
                              histname=histname): (0.0, 8.0),
            DataVault().input(production, "high",
                              histname=histname): (4.0, 20.0)
        }

        options = CompositeNonlinearityOptions(unified_inputs)
        options.fitf = None
        options.factor = 1.
        estimator = Nonlinearity(options)
        loggs = AnalysisOutput("optimal nonlinearity")
        nonlinearity = estimator.transform(
            [
                DataVault().input("data", listname="Phys",
                                  histname="MassPt"),
                unified_inputs
            ],
            loggs=loggs
        )
        loggs.plot()
        # Comparator().compare(nonlinearity)
