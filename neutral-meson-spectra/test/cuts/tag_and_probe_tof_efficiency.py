import unittest
import ROOT
import sys

from spectrum.sutils import get_canvas
from spectrum.input import Input
from spectrum.invariantmass import InvariantMass


# TODO: divide this class into tagandprobe and tagandprobeinput

class TagAndProbe(object):
    def __init__(self, filename, selname, histname, cut, full):
        super(TagAndProbe, self).__init__()
        self.selection = selname
        self.erange = (0, 20)
        self.ispi0 = 'pi0'
        self.fixedcb = True
        self.nsigma = 3

        self.full = self.read(filename, histname, full)
        self.full.Draw()

        self.cut = self.read(filename, histname, cut)
        self.cut.Draw()

        raw_input('...')

    def read(self, filename, histname, ending):
        reader = Input(filename, self.selection, histname % ending)
        nevents, hist, dummy = reader.read()
        return hist

    def calculate_range(self, hist):
        mass = InvariantMass(hist, hist, self.erange, self.ispi0, self.fixedcb)
        peak, bgrnd = mass.noisy_peak_parameters()

        mass, sigma = peak[1], peak[2]
        return (mass - self.nsigma * sigma, mass + self.nsigma * sigma)

    def probe_spectrum(self, hist, mrange):
        a, b = map(hist.GetXaxis().FindBin, mrange)
        mass = hist.ProjectionY(hist.GetName() + '_%d_%d' % (a, b), a, b)
        # TODO: add suffix here TOF, All
        mass.SetTitle('Probe distribution #events = %d M; M_{#gamma#gamma}, GeV/c^{2}' % (hist.nevents / 1e6))         
        mass.SetLineColor(37)
        return mass        

    def estimate(self):
        fullrange = self.calculate_range(self.full)
        full = self.probe_spectrum(self.full, fullrange)
        full.Draw()

        cutrange = self.calculate_range(self.cut)
        cut = self.probe_spectrum(self.cut, cutrange)
        cut.Draw('same')
        raw_input('...')

        cut.Divide(full)
        cut.Draw()
        raw_input('...')




class TagAndProbeEfficiencyTOF(unittest.TestCase):

    def setUp(self):
        self.eff_calculator = TagAndProbe('input-data/LHC16h-muon-calo-pass1.root', 'TOFStudyTender', 'MassEnergy%s_SM0', cut='TOF', full='All')

    def testCompareResults(self):
        self.eff_calculator.estimate()



if __name__ == '__main__':
    main()