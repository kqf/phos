import ROOT
import unittest

from vault.formulas import FVault
from spectrum.comparator import Comparator


class TestTsallisFunction(unittest.TestCase):

    def test_parameters(self):
        fv = FVault()
        functions = [
            ROOT.TF1('f' + str(i), fv.func("tsallis"), 0, 20)
            for i in range(3)
        ]

        parameters = [
            0.014960701090585591,
            0.287830380417601,
            9.921003040859755
        ]

        for change in [0, 1, 2]:
            ROOT.gStyle.SetPalette(51)
            for i, func in enumerate(functions):
                for ip, par in enumerate(parameters):
                    parvalue = par + 10 * i * (change == ip)
                    func.SetParameter(ip, parvalue)
                    func.SetLineColor(i + 1)

                func.Draw("same" if i != 0 else "apl")

            Comparator().compare(
                map(lambda x: x.GetHistogram(), functions)
            )
