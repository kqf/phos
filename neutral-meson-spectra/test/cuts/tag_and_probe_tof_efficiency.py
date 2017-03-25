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
from spectrum.options import Options


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
    with open('config/spectrum.json') as f:
        conf = json.load(f)

    def __init__(self, filename, selname, histname, cut, full):
        super(TagAndProbe, self).__init__()
        self.cut_and_full = self.get_estimators(filename, selname, histname, cut, full)
        self.ispi0 = 'pi0'
        self.erange = conf["erange"]
        self.nsigma = conf["nsigma"]


    def get_estimators(self, filename, selname, histname, cut, full):
        f = lambda x : ProbeSpectrum(filename, selname, histname, x, self.erange, Options(relaxedcb = True), self.nsigma)
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
        f = lambda x : Spectrum(Input(filename, selname, histname % x).read(), x, 'q', self.nsigma, Options(relaxedcb = True))
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
        self.infile = 'input-data/LHC16-new.root'
        self.sel = 'TOFStudyTender'
        self.eff_calculator = TagAndProbeRigorous(self.infile, self.sel, 'MassEnergy%s_SM0', cut='TOF', full='All')
        self.eff_calculator_relaxed = TagAndProbe(self.infile, self.sel, 'MassEnergy%s_SM0', cut='TOF', full='All')

    def testEstimateEfficiency(self):
        res = self.eff_calculator.estimate()

        # Decorate
        f = lambda x: x.SetTitle('Energy spectrum of probe photons; E_{#gamma}, GeV')
        map(f, res)

        diff = Comparator()
        diff.compare_set_of_histograms([[i] for i in res])

    @unittest.skip('Debug')
    def testCompareEfficienciesDifferentMethods(self):
        cut, full = self.eff_calculator.estimate()
        eff1 = ratio(cut, full, 'TOF efficiency; E, GeV', 'rigorous')

        cut, full = self.eff_calculator_relaxed.estimate()
        eff2 = ratio(cut, full, 'TOF efficiency; E, GeV', 'simple')
        
        diff = Comparator()
        diff.compare_set_of_histograms([[eff1], [eff2]])

    @unittest.skip('Debug')
    def testDifferentModules(self):
        estimators = [TagAndProbeRigorous(self.infile, self.sel, 'MassEnergy%s' + '_SM%d' % i, cut='TOF', full='All') for i in range(1, 3)]
        f = lambda i, x, y: ratio(x, y, 'TOF efficiency in different modules; E, GeV', 'SM%d' % i)
        multiple = [[f(i + 1, *(e.estimate()))] for i, e in enumerate(estimators)]

        # TODO: add tag and probe method for different modules
        #       fix the problem with axis.
        #       investigate the problem with module1
        c1 = get_canvas()
        diff = Comparator()
        diff.compare_set_of_histograms(multiple)



if __name__ == '__main__':
    main()