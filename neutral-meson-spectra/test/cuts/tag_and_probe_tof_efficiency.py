import unittest
import ROOT
import sys
import json
from spectrum.sutils import get_canvas, wait, area_and_error, ratio
from spectrum.input import Input
from spectrum.invariantmass import InvariantMass
from spectrum.comparator import Comparator
from spectrum.spectrum import Spectrum
from spectrum.ptanalyzer import PtDependent


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
        hist, dummy = reader.read()
        return hist


    def calculate_range(self, hist):
        canvas = get_canvas()
        mass = InvariantMass((hist, hist), self.erange, 1, self.ispi0, self.relaxedcb)
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


    def spectrum(self, edges):
        fullrange = self.calculate_range(self.hist)
        spectr = self.probe_spectrum(self.hist, fullrange)

        edges = arr.array('d', edges)
        spectr = spectr.Rebin(len(edges) - 1, spectr.GetName() + "_rebinned", edges)
        spectr.label = self.pref
        spectr.logy = True
        return spectr


# TODO: write config for this analysis (TagAndProbe)
class TagAndProbe(object):
    def __init__(self, filename, selname, histname, cut, full):
        super(TagAndProbe, self).__init__()
        self.erange = (0, 20)
        self.ispi0 = 'pi0'
        self.nsigma = 3
        self.cut_and_full = self.get_estimators(filename, selname, histname, cut, full)

    def get_estimators(self, filename, selname, histname, cut, full):
        f = lambda x : ProbeSpectrum(filename, selname, histname, x, self.erange, self.ispi0, self.nsigma)
        return map(f, [cut, full])
  
    def estimate(self):
        edges, rebins = self.get_bins_rebins()
        f = lambda x: x.spectrum(edges)
        return map(f, self.cut_and_full)

    def get_bins_rebins(self):
        """
            get_bins_rebins -- returns array of edges and 
            array of bins that should be rebinned
        """
        with open('config/pt-analysis.json') as f:
            conf = json.load(f)
        props = conf[self.ispi0]
        return props['ptedges'], props['need_rebin']



class TagAndProbeRigorous(TagAndProbe):
    def __init__(self, filename, selname, histname, cut, full):
        super(TagAndProbeRigorous, self).__init__(filename, selname, histname, cut, full)

    def get_estimators(self, filename, selname, histname, cut, full):
        f = lambda x : Spectrum(Input(filename, selname, histname % x).read(), x, 'q', self.nsigma, self.ispi0, relaxedcb = True)
        return map(f, [cut, full])

    def probe_spectrum(self, estimator):
        mranges = estimator.mass_ranges()
        results = map(lambda x, y: area_and_error(x.mass, *y), estimator.analyzer.masses, mranges)
        ehist = PtDependent('spectrum', 'probe distribution; E, GeV', estimator.analyzer.label)
        return ehist.get_hist(estimator.analyzer.divide_into_bins()[0], results, True)

    def estimate(self):
        return map(self.probe_spectrum, self.cut_and_full)



class TagAndProbeEfficiencyTOF(unittest.TestCase):

    def setUp(self):
        self.canvas = get_canvas()
        self.eff_calculator = TagAndProbeRigorous('input-data/LHC16k-pass1.root', 'TOFStudyTender', 'MassEnergy%s_SM0', cut='TOF', full='All')
        self.eff_calculator_relaxed = TagAndProbe('input-data/LHC16k-pass1.root', 'TOFStudyTender', 'MassEnergy%s_SM0', cut='TOF', full='All')

    def testEstimateEfficiency(self):
        cut, full = self.eff_calculator.estimate()
        
        diff = Comparator()
        diff.compare_set_of_histograms([[cut], [full]])

    def testCompareEfficienciesDifferentMethods(self):
        cut, full = self.eff_calculator.estimate()
        eff1 = ratio(cut, full, 'TOF efficiency; E, GeV', 'rigorous')

        cut, full = self.eff_calculator_relaxed.estimate()
        eff2 = ratio(cut, full, 'TOF efficiency; E, GeV', 'simple')
        
        diff = Comparator()
        diff.compare_set_of_histograms([[eff1], [eff2]])



if __name__ == '__main__':
    main()