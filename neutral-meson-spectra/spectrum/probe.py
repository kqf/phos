import json
import ROOT

from sutils import gcanvas, wait
from .input import Input
from invariantmass import InvariantMass
from spectrum import Spectrum
from options import Options
from outputcreator import OutputCreator

from broot import BROOT as br

ROOT.TH1.AddDirectory(False)

class ProbeSpectrum(object):
    def __init__(self, filename, selname, histname, pref, erange, nsigma, options):
        super(ProbeSpectrum, self).__init__()
        self.selection = selname
        self.erange = erange
        self.nsigma = nsigma
        self.pref = pref
        self.options = options
        self.hist = self.read(filename, histname, pref)


    def read(self, filename, histname, ending):
        reader = Input(filename, self.selection, histname % ending)
        hist, dummy = reader.read()
        return hist


    def calculate_range(self, hist):
        canvas = gcanvas()
        mass = InvariantMass((hist, hist), tuple(self.erange), 1, self.options)
        peak, bgrnd = mass.noisy_peak_parameters()
        wait('single-tag-tof-mass-fit-' + self.pref, True, True)

        mass, sigma = peak[1], peak[2]
        return (mass - self.nsigma * sigma, mass + self.nsigma * sigma)


    def probe_spectrum(self, hist, mrange):
        a, b = map(hist.GetXaxis().FindBin, mrange)
        mass = br.project_range(hist, '_e_%d_%d', *mrange, axis = 'y')
        mass.SetTitle('Probe distribution, %s #events = %d M; M_{#gamma#gamma}, GeV/c^{2}' % (self.pref, hist.nevents / 1e6))         
        mass.SetLineColor(46)
        mass.SetStats(False)
        return mass        


    def spectrum(self, edges):
        fullrange = self.calculate_range(self.hist)
        spectr = self.probe_spectrum(self.hist, fullrange)

        # Rebin the spectrum, check if spectr has properties
        spectr = br.rebin(spectr, edges)
        spectr.label = self.pref
        spectr.logy = True
        return spectr


class TagAndProbe(object):


    def __init__(self, filename, selname, histname, cut, full, conffile = 'config/test_tagandprobe.json'):
        super(TagAndProbe, self).__init__()
        self.conffile = conffile 
        with open(self.conffile) as f:
            conf = json.load(f)

        self.ispi0  = conf["particle"]
        self.erange = conf["erange"]
        self.nsigma = conf["nsigma"]

        prop = conf[self.ispi0]
        self.ptedges = prop["ptedges"]
        self.need_rebin = prop["need_rebin"]
        self.cut_and_full = self.get_estimators(filename, selname, histname, cut, full)


    def get_estimators(self, filename, selname, histname, cut, full):
        f = lambda x : ProbeSpectrum(filename, selname, histname, x, self.erange, self.nsigma, Options(relaxedcb = True))
        return map(f, [cut, full])
  

    def estimate(self):
        f = lambda x: x.spectrum(self.ptedges)
        return map(f, self.cut_and_full)



class TagAndProbeRigorous(TagAndProbe):
    def __init__(self, filename, selname, histname, cut, full, conffile = 'config/test_tagandprobe.json'):
        super(TagAndProbeRigorous, self).__init__(filename, selname, histname, cut, full,  conffile)

    def get_estimators(self, filename, selname, histname, cut, full):
        def f(x):
            options = Options(x, 'q', relaxedcb = True)
            options.spectrum.nsigmas = self.nsigma
            options.pt.config = self.conffile
            inp = Input(filename, selname, histname % x).read()
            return Spectrum(inp, options)

        estimators = map(f, [cut, full])
        return estimators

    def probe_spectrum(self, estimator):
        mranges = estimator.mass_ranges()
        results = map(lambda x, y: br.area_and_error(x.mass, *y), estimator.analyzer.masses, mranges)
        ehist = OutputCreator('spectrum', 'probe distribution; E, GeV', estimator.analyzer.opt.label)
        ehist = ehist.get_hist(estimator.analyzer.opt.ptedges, results)
        ehist.logy = True
        return ehist


    def estimate(self)  :
        return map(self.probe_spectrum, self.cut_and_full)
