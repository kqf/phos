import unittest
import ROOT

from spectrum.comparator import Comparator
from spectrum.input import SingleHistInput
from vault.datavault import DataVault
from spectrum.broot import BROOT as br


def fit_function(particle):
    tsallis = ROOT.TF1("f", "(x[0] )*[0]/2./3.1415*([2]-1.)*([2]-2.)/([2]*[1]*([2]*[1]+[4]*([2]-2.))) * (1.+(sqrt((x[0])*(x[0])+[3]*[3])-[4])/([2]*[1])) ** (-[2])", 0, 20);

    # No Weights
    # tsallis.SetParameters(2.4, 0.139, 6.880);

    # Weights0
    # tsallis.SetParameters(0.014948507575731244, 0.2874438247098432, 9.895472915554668)

    # Weights1
    tsallis.SetParameters(0.014960701090585591, 0.287830380417601, 9.921003040859755)
                         # [0.014850211992453644, 0.28695967166609104, 9.90060126848571

    tsallis.FixParameter(3, 0.135);
    tsallis.FixParameter(4, 0.135);
    tsallis.SetLineColor(46)
    return tsallis




class TestGeneratedDistribution(unittest.TestCase):

	def test_generated_distribution(self):
		data = "low", "high"
		for prod in data:
			function = fit_function("#pi^{0}")
			generated = SingleHistInput('hPt_#pi^{0}_primary_standard').transform(
				DataVault().input("single #pi^{0} iteration3 new tender", prod)
			)
			generated.Scale(1. / generated.Integral())
			diff = Comparator()
			diff.compare(generated, function)


