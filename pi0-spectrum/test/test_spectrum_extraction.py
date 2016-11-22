
import unittest
import ROOT

# Todo: try to avoid this function here.
def my_input(filename):
    lst = ROOT.TFile(filename).PhysNoTender
    nevents = lst.FindObject('TotalEvents').GetEntries()
    rawhist = lst.FindObject('hMassPtN3')
    rawmix = lst.FindObject('hMixMassPtN3')
    return [nevents, rawhist, rawmix]

class TestSpectrum(unittest.TestCase):

	def testPi0SpectrumLHC16k(self):
		# These are values calculated by standard algorithm.
		# Make sure that you have the same copy of LHC16k.root file. 
		# sha sum: 535b8fd27f6c54dd74687a93c5cf192c142c1384
		# This is to test the code after refactoring.

		nominal = [[0.1322653591632843, 0.13277405500411987, 0.13303369283676147, 0.13313989341259003, 0.13352960348129272, 0.13362841308116913, 0.1339358687400818, 0.134202778339386, 0.1344127655029297, 0.13470493257045746, 0.1347610056400299, 0.1350044459104538, 0.1352168321609497, 0.13549686968326569, 0.13572010397911072, 0.13577601313591003, 0.13574261963367462, 0.13630534708499908, 0.13658511638641357, 0.13676218688488007, 0.13694633543491364, 0.13655047118663788, 0.13630391657352448, 0.13537542521953583, 0.13741467893123627, 0.1381002962589264, 0.13742034137248993, 0.13746903836727142, 0.13881348073482513, 0.13958445191383362, 0.1371551752090454, 0.1397911012172699],
		[0.008401956409215927, 0.008161904290318489, 0.007177543826401234, 0.006798639427870512, 0.006754352245479822, 0.006405044347047806, 0.00616020243614912, 0.006039798725396395, 0.006147556006908417, 0.006151742767542601, 0.005708953365683556, 0.005743146874010563, 0.005802936386317015, 0.006137227639555931, 0.005848325788974762, 0.006021082401275635, 0.005979498848319054, 0.005106013733893633, 0.005664974916726351, 0.005000488366931677, 0.005610583815723658, 0.00497478898614645, 0.0057155373506248, 0.005519375205039978, 0.005459747742861509, 0.005686728749424219, 0.004451272543519735, 0.0060568335466086864, 0.005163443740457296, 0.005660128779709339, 0.0057741208001971245, 0.004000001586973667],
		[580.5882568359375, 1994.054931640625, 2085.60888671875, 1933.4752197265625, 1619.7523193359375, 1311.1973876953125, 1047.683837890625, 837.39599609375, 670.2992553710938, 546.0557861328125, 414.5222473144531, 330.6585693359375, 270.9864501953125, 225.99887084960938, 186.10647583007812, 157.24163818359375, 90.85311126708984, 51.45967102050781, 37.9100456237793, 22.99233055114746, 17.432775497436523, 10.280006408691406, 7.00640869140625, 5.369962692260742, 5.626502513885498, 4.091230392456055, 2.29396915435791, 2.2896952629089355, 1.167350172996521, 0.8340329527854919, 0.5255765914916992, 0.23293808102607727],
		[1.3545184135437012, 2.071387767791748, 1.9930912256240845, 2.2921531200408936, 2.554793357849121, 2.2817423343658447, 1.6304713487625122, 1.6575069427490234, 1.4818781614303589, 1.4715896844863892, 1.3429985046386719, 1.1783673763275146, 1.2725285291671753, 1.8231711387634277, 0.9900429248809814, 1.4492956399917603, 1.4919641017913818, 1.633657455444336, 1.1368465423583984, 1.2906041145324707, 1.2713207006454468, 2.8378617763519287, 1.3868142366409302, 1.6704952716827393, 1.4146642684936523, 1.058394193649292, 0.7523159384727478, 0.6971927285194397, 0.6850036382675171, 0.8025014996528625, 0.978635847568512, 0.6074792146682739]]

		from spectrum.spectrum import PtAnalyzer

		second = PtAnalyzer(my_input('input-data/LHC16k.root'), label = 'Mixing', mode = 'q').quantities()
		actual = [ [ h.GetBinContent(i) for i in range(1, h.GetNbinsX())] for h in second]

		for a, b, c in zip(nominal, actual, second):
				print 'Checking ', c.GetName()
				for aa, bb in zip(a, b): self.assertAlmostEqual(aa, bb)