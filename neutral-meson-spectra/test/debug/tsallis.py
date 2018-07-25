import unittest
import ROOT

from vault.datavault import DataVault
from vault.formulas import FVault
from spectrum.comparator import Comparator
from spectrum.input import SingleHistInput
from spectrum.broot import BROOT as br


class DebugTheEfficiency(unittest.TestCase):

    def test_weight_like_debug(self):
        input_low = DataVault().input(
            "debug efficiency", "low", n_events=1e6,
            histnames=('hSparseMgg_proj_0_1_3_yx', ''))

        # Define the transformations
        nominal_low = SingleHistInput("hGenPi0Pt_clone").transform(input_low)

        rrange = 0, 20
        tsallis = ROOT.TF1("f", FVault().func("tsallis"), *rrange)
        parameters = [0.6216964179825611 / 0.0989488446585,
                      0.1327837274571318,
                      6.656459891593017,
                      0.135,
                      0.135]
        for i, p in enumerate(parameters):
            tsallis.FixParameter(i, p)
        tsallis.FixParameter(3, 0.135)
        tsallis.FixParameter(4, 0.135)
        tsallis.SetLineColor(ROOT.kRed + 1)

        br.scalew(nominal_low)
        nominal_low.Scale(1. / nominal_low.Integral())
        nominal_low.Fit(tsallis)
        nominal_low.logy = True
        print tsallis.GetChisquare() / tsallis.GetNDF()
        print br.pars(tsallis)
        Comparator().compare(nominal_low)
        print tsallis.Integral(0, 20)
