
import unittest
import ROOT
import sys

from spectrum.spectrum import PtAnalyzer
from spectrum.spectrum import Spectrum
from spectrum.options import Options
from spectrum.input import Input

class TestSpectrum(unittest.TestCase):


	def setUp(self):
		# Different values in some pt-bins can be explained by limited statistics in those bins.
		#

		# Important:
		# This one should be set explicitely otherwise the test will fail
		# Because this global variable is set to Minuit2 in other tests
		ROOT.TVirtualFitter.SetDefaultFitter('Minuit')
		
		# NB: test Spectrum class, not Pt-dependent as it produces negative values due to wide integration range
		# Expected values for $\pi^0$ extraction


		linux = [[0.1385035365819931, 0.1379297524690628, 0.1377740353345871, 0.1376171112060547, 0.13748160004615784, 0.13741150498390198, 0.13734154403209686, 0.13733915984630585, 0.13732565939426422, 0.1372251659631729, 0.1372394561767578, 0.13733479380607605, 0.13733546435832977, 0.13738012313842773, 0.13735418021678925, 0.1372484415769577, 0.13729068636894226, 0.13753274083137512, 0.13743533194065094, 0.1372087448835373, 0.13751940429210663, 0.1376037895679474, 0.13750572502613068, 0.13752663135528564, 0.1381254941225052, 0.13781097531318665, 0.1366795152425766, 0.1373700648546219, 0.13841138780117035, 0.13771122694015503, 0.13830219209194183, 0.13682211935520172], [0.006829891353845596, 0.00648513762280345, 0.0061491564847528934, 0.005654092878103256, 0.0054403431713581085, 0.005305469036102295, 0.00503291143104434, 0.0049264440312981606, 0.004919453989714384, 0.0048954663798213005, 0.004712176974862814, 0.0045048245228827, 0.00451483391225338, 0.004503644537180662, 0.004350554198026657, 0.004293032921850681, 0.004397036507725716, 0.00440073199570179, 0.004360508639365435, 0.0043545858934521675, 0.004232915583997965, 0.004635291174054146, 0.0047595808282494545, 0.004636007826775312, 0.004053359851241112, 0.0042190407402813435, 0.004000000189989805, 0.004000000189989805, 0.004000000189989805, 0.004037226550281048, 0.005423584952950478, 0.0040000006556510925], [6269.55224609375, 11516.8115234375, 15535.4033203125, 16932.74609375, 16845.482421875, 15300.5234375, 13515.724609375, 11538.1953125, 9652.109375, 8095.9892578125, 6575.33056640625, 5410.42431640625, 4508.01806640625, 3737.694091796875, 3114.85791015625, 2542.988525390625, 1155.656005859375, 1002.0328369140625, 532.95068359375, 451.97918701171875, 250.4065399169922, 230.58523559570312, 130.8486785888672, 128.6576385498047, 65.09651184082031, 62.08954620361328, 38.735374450683594, 40.585636138916016, 17.664045333862305, 12.346247673034668, 7.2027153968811035, 2.602996349334717], [0.9572145938873291, 1.185160517692566, 1.5655676126480103, 1.271836519241333, 1.5575073957443237, 1.6774957180023193, 1.7059613466262817, 1.5260553359985352, 1.4281840324401855, 1.2834032773971558, 1.3695411682128906, 1.4419063329696655, 1.3717505931854248, 1.1325606107711792, 1.1835919618606567, 0.9675224423408508, 1.0349256992340088, 1.146649718284607, 0.82023024559021, 0.9522941708564758, 1.193197250366211, 1.1683934926986694, 1.028658151626587, 1.404440999031067, 0.8370833992958069, 0.9262980222702026, 0.6871531009674072, 0.6397743821144104, 0.6954476237297058, 0.610698938369751, 0.6351824402809143, 0.5916465520858765], [1.4930000305175781, 1.4930000305175781, 1.4930000305175781, 1.4930000305175781, 1.4930000305175781, 1.4930000305175781, 1.4930000305175781, 1.4930000305175781, 1.4930000305175781, 1.4930000305175781, 1.4930000305175781, 1.4930000305175781, 1.4930000305175781, 1.4930000305175781, 1.4930000305175781, 1.4930000305175781, 1.4930000305175781, 1.4930000305175781, 1.4930000305175781, 1.4930000305175781, 1.4930000305175781, 1.4930000305175781, 1.4930000305175781, 1.4930000305175781, 1.4930000305175781, 1.4930000305175781, 1.4930000305175781, 1.4930000305175781, 1.4930000305175781, 1.4930000305175781, 1.4930000305175781, 1.4930000305175781], [1.5959999561309814, 1.5959999561309814, 1.5959999561309814, 1.5959999561309814, 1.5959999561309814, 1.5959999561309814, 1.5959999561309814, 1.5959999561309814, 1.5959999561309814, 1.5959999561309814, 1.5959999561309814, 1.5959999561309814, 1.5959999561309814, 1.5959999561309814, 1.5959999561309814, 1.5959999561309814, 1.5959999561309814, 1.5959999561309814, 1.5959999561309814, 1.5959999561309814, 1.5959999561309814, 1.5959999561309814, 1.5959999561309814, 1.5959999561309814, 1.5959999561309814, 1.5959999561309814, 1.5959999561309814, 1.5959999561309814, 1.5959999561309814, 1.5959999561309814, 1.5959999561309814, 1.5959999561309814]]
		macos = [[0.1385035365819931, 0.1379297524690628, 0.1377740353345871, 0.1376171112060547, 0.13748160004615784, 0.13741150498390198, 0.13734154403209686, 0.13733915984630585, 0.13732565939426422, 0.1372251659631729, 0.1372394561767578, 0.13733479380607605, 0.13733546435832977, 0.13738012313842773, 0.13735418021678925, 0.1372484415769577, 0.13729068636894226, 0.13753274083137512, 0.13743533194065094, 0.1372087448835373, 0.13751940429210663, 0.1376037895679474, 0.13750572502613068, 0.13752663135528564, 0.1381254941225052, 0.13781097531318665, 0.1366795152425766, 0.1373700648546219, 0.13841138780117035, 0.13771122694015503, 0.13830219209194183, 0.13682672381401062], [0.006829891353845596, 0.00648513762280345, 0.0061491564847528934, 0.005654092878103256, 0.0054403431713581085, 0.005305469036102295, 0.00503291143104434, 0.0049264440312981606, 0.004919453989714384, 0.0048954663798213005, 0.004712176974862814, 0.0045048245228827, 0.00451483391225338, 0.004503644537180662, 0.004350554198026657, 0.004293032921850681, 0.004397036507725716, 0.00440073199570179, 0.004360508639365435, 0.0043545858934521675, 0.004232915583997965, 0.004635291174054146, 0.0047595808282494545, 0.004636007826775312, 0.00405335845425725, 0.0042190407402813435, 0.004000000189989805, 0.004000000189989805, 0.004000000189989805, 0.004037226550281048, 0.005423584952950478, 0.0040000006556510925], [5753.26025390625, 11003.294921875, 14774.6650390625, 16568.9921875, 16494.384765625, 15300.5234375, 13515.724609375, 11538.1953125, 9652.109375, 8095.9892578125, 6729.72119140625, 5542.1396484375, 4617.3857421875, 3822.056640625, 3181.2890625, 2595.468994140625, 1185.2474365234375, 1027.0003662109375, 546.4692993164062, 461.4468994140625, 254.32981872558594, 235.9136962890625, 133.3511505126953, 131.2930908203125, 66.50995635986328, 65.29728698730469, 40.420372009277344, 41.65175247192383, 17.814247131347656, 12.40540599822998, 7.680180549621582, 2.561617851257324], [0.9572145938873291, 1.185160517692566, 1.5655676126480103, 1.271836519241333, 1.5575073957443237, 1.6774957180023193, 1.7059613466262817, 1.5260553359985352, 1.4281840324401855, 1.2834032773971558, 1.3695411682128906, 1.4419063329696655, 1.3717505931854248, 1.1325606107711792, 1.1835919618606567, 0.9675224423408508, 1.0349256992340088, 1.146649718284607, 0.82023024559021, 0.9522941708564758, 1.193197250366211, 1.1683934926986694, 1.028658151626587, 1.404440999031067, 0.8370832800865173, 0.9262980222702026, 0.6871531009674072, 0.6397742033004761, 0.6954476237297058, 0.6106991171836853, 0.6351824402809143, 0.5899117588996887], [1.4930000305175781, 1.4930000305175781, 1.4930000305175781, 1.4930000305175781, 1.4930000305175781, 1.4930000305175781, 1.4930000305175781, 1.4930000305175781, 1.4930000305175781, 1.4930000305175781, 1.4930000305175781, 1.4930000305175781, 1.4930000305175781, 1.4930000305175781, 1.4930000305175781, 1.4930000305175781, 1.4930000305175781, 1.4930000305175781, 1.4930000305175781, 1.4930000305175781, 1.4930000305175781, 1.4930000305175781, 1.4930000305175781, 1.4930000305175781, 1.4930000305175781, 1.4930000305175781, 1.4930000305175781, 1.4930000305175781, 1.4930000305175781, 1.4930000305175781, 1.4930000305175781, 1.4930000305175781], [1.5959999561309814, 1.5959999561309814, 1.5959999561309814, 1.5959999561309814, 1.5959999561309814, 1.5959999561309814, 1.5959999561309814, 1.5959999561309814, 1.5959999561309814, 1.5959999561309814, 1.5959999561309814, 1.5959999561309814, 1.5959999561309814, 1.5959999561309814, 1.5959999561309814, 1.5959999561309814, 1.5959999561309814, 1.5959999561309814, 1.5959999561309814, 1.5959999561309814, 1.5959999561309814, 1.5959999561309814, 1.5959999561309814, 1.5959999561309814, 1.5959999561309814, 1.5959999561309814, 1.5959999561309814, 1.5959999561309814, 1.5959999561309814, 1.5959999561309814, 1.5959999561309814, 1.5959999561309814]]
		self.nominal_pi0 = macos if 'darwin' in sys.platform else linux

		# Expected values for $\eta$ extraction
		elinux = [[0.5504456758499146, 0.5583246946334839, 0.5675840377807617, 0.5538944005966187, 0.5595543384552002, 0.5624135136604309, 0.5626147389411926, 0.555587112903595, 0.5546109676361084, 0.5594231486320496], [0.004980900324881077, 0.0088952099904418, 0.012779376469552517, 0.030589519068598747, 0.019996635615825653, 0.016347546130418777, 0.0169938113540411, 0.016152609139680862, 0.010123957879841328, 0.013841118663549423], [39.19988250732422, 129.62466430664062, 114.57780456542969, 146.80050659179688, 157.1143035888672, 125.38175964355469, 95.31459045410156, 29.153339385986328, 9.655427932739258, 6.313199996948242], [0.6729754209518433, 1.139630675315857, 1.0028939247131348, 0.6992102265357971, 0.8957198262214661, 0.8177729845046997, 1.0520663261413574, 1.0081721544265747, 0.8329330682754517, 0.8705211877822876], [1.1794236898422241, 1.1794236898422241, 1.1794236898422241, 1.1794236898422241, 1.1794236898422241, 1.1794236898422241, 1.1794236898422241, 1.1794236898422241, 1.1794236898422241, 1.1794236898422241], [2.669532060623169, 2.669532060623169, 2.669532060623169, 2.669532060623169, 2.669532060623169, 2.669532060623169, 2.669532060623169, 2.669532060623169, 2.669532060623169, 2.669532060623169]]
		emacos = [[0.5504664778709412, 0.5583181977272034, 0.5612748265266418, 0.5542241334915161, 0.5593482255935669, 0.5623841285705566, 0.5623455047607422, 0.5552688241004944, 0.5545464754104614, 0.5587753653526306], [0.0049341958947479725, 0.008887356147170067, 0.009073580615222454, 0.02622056193649769, 0.020479613915085793, 0.016146712005138397, 0.017273275181651115, 0.016502588987350464, 0.010240375064313412, 0.014565246179699898], [49.50495147705078, 130.43258666992188, 100.61174774169922, 145.43145751953125, 141.23605346679688, 101.47055053710938, 77.80941009521484, 27.702444076538086, 8.739906311035156, 5.397545337677002], [0.6749923229217529, 1.139954924583435, 0.6573015451431274, 0.5322279334068298, 0.8988932371139526, 0.822588324546814, 1.051897644996643, 1.015588402748108, 0.8375778794288635, 0.8705666661262512], [1.4930000305175781, 1.4930000305175781, 1.4930000305175781, 1.4930000305175781, 1.4930000305175781, 1.4930000305175781, 1.4930000305175781, 1.4930000305175781, 1.4930000305175781, 1.4930000305175781], [1.5959999561309814, 1.5959999561309814, 1.5959999561309814, 1.5959999561309814, 1.5959999561309814, 1.5959999561309814, 1.5959999561309814, 1.5959999561309814, 1.5959999561309814, 1.5959999561309814]]
		self.nominal_eta = emacos if 'darwin' in sys.platform else elinux

		# Make sure that you have the same copy of LHC16.root file. 
		# sha 256 sum: a340256c4138894412ea87df53e5813fd92c3f90bd0e06883a18bef49ebf4c90
		# This is to test the code after refactoring.
		self.infile = 'input-data/LHC16.root'



	def testPi0SpectrumLHC16(self):
		second = Spectrum(Input(self.infile, 'PhysTender').read(), label = 'testsignal', mode = 'q').evaluate()
		actual = [ [ h.GetBinContent(i) for i in range(1, h.GetNbinsX())] for h in second]

		for a, b, c in zip(self.nominal_pi0, actual, second):
			print 'Checking ', c.GetName()
			for aa, bb in zip(a, b): self.assertAlmostEqual(aa, bb)
		# TODO: add other number of pi0s	

	def testEtaSpectrumLHC16(self):
		indata = Input(self.infile, 'EtaTender')
		analysis = Spectrum(indata.read(), 'testsignal', 'q', options = Options(particle='eta'))
		histograms = analysis.evaluate()
		
		actual = [[h.GetBinContent(i) for i in range(1, h.GetNbinsX())] for h in histograms]
		print actual

		for a, b, c in zip(self.nominal_eta, actual, histograms):
			print 'Checking ', c.GetName()
			for aa, bb in zip(a, b): self.assertAlmostEqual(aa, bb)

