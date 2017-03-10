import unittest
import ROOT
import sys

from spectrum.sutils import get_canvas, wait
from spectrum.input import Input
from spectrum.invariantmass import InvariantMass
from spectrum.comparator import Comparator


import numpy as np
import array as arr

ROOT.TH1.AddDirectory(False)

class ProbeSpectrum(object):
    def __init__(self, filename, selname, histname, pref, erange, ispi0, nsigma):
        super(ProbeSpectrum, self).__init__()
        self.selection = selname
        self.erange = erange
        self.ispi0 = ispi0
        self.relaxedcb = True
        self.nsigma = nsigma
        self.pref = pref
        self.hist = self.read(filename, histname, pref)


    def read(self, filename, histname, ending):
        reader = Input(filename, self.selection, histname % ending)
        nevents, hist, dummy = reader.read()
        return hist


    def calculate_range(self, hist):
        canvas = get_canvas()
        mass = InvariantMass(hist, hist, self.erange, 1, self.ispi0, self.relaxedcb)
        peak, bgrnd = mass.noisy_peak_parameters()
        wait('single-tag-tof-mass-fit-' + self.pref, True, True)

        mass, sigma = peak[1], peak[2]
        return (mass - self.nsigma * sigma, mass + self.nsigma * sigma)


    def probe_spectrum(self, hist, mrange):
        a, b = map(hist.GetXaxis().FindBin, mrange)
        mass = hist.ProjectionY(hist.GetName() + '_e_%d_%d' % (a, b), a, b)
        mass.SetTitle('Probe distribution, %s #events = %d M; M_{#gamma#gamma}, GeV/c^{2}' % (self.pref, hist.nevents / 1e6))         
        mass.SetLineColor(46)
        mass.SetStats(False)
        return mass        


    def spectrum(self):
        fullrange = self.calculate_range(self.hist)
        spectr = self.probe_spectrum(self.hist, fullrange)

        edges = arr.array('d', np.logspace(np.log10(1), np.log10(20), 20))
        spectr = spectr.Rebin(len(edges) - 1, spectr.GetName() + "_rebinned", edges)
        spectr.label = self.pref
        spectr.logy = True
        return spectr


class TagAndProbe(object):
    def __init__(self, filename, selname, histname, cut, full):
        super(TagAndProbe, self).__init__()
        self.erange = (0, 20)
        self.ispi0 = 'pi0'
        self.nsigma = 3

        f = lambda x : ProbeSpectrum(filename, selname, histname, x, self.erange, self.ispi0, self.nsigma)
        self.cut_and_full = map(f, [cut, full])

    def estimate(self):
        f = lambda x: x.spectrum()
        return map(f, self.cut_and_full)



class TagAndProbeEfficiencyTOF(unittest.TestCase):

    def setUp(self):
        self.canvas = get_canvas()
        self.eff_calculator = TagAndProbe('input-data/LHC16h-muon-calo-pass1.root', 'TOFStudyTender', 'MassEnergy%s_SM0', cut='TOF', full='All')

    def testCompareResults(self):
        cut, full = self.eff_calculator.estimate()
        
        diff = Comparator()
        diff.compare_set_of_histograms([[cut], [full]])






if __name__ == '__main__':
    main()