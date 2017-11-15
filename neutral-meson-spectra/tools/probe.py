import json
import ROOT

from spectrum.input import Input
from spectrum.options import Options
from spectrum.spectrum import Spectrum
from spectrum.sutils import gcanvas, wait
from spectrum.invariantmass import InvariantMass
from spectrum.outputcreator import OutputCreator
from spectrum.comparator import Comparator

from spectrum.broot import BROOT as br

ROOT.TH1.AddDirectory(False)

# TODO: Draw corrected version with invariant mass

class TagAndProbe(object):
    def __init__(self, sinput, nsigmas, cut_nocut = ('TOF', 'All')):
        super(TagAndProbe, self).__init__()
        self.hpattern = sinput.histname
        self.nsigmas = nsigmas
        self.input = sinput
        self.cut_and_full = map(self._estimator, cut_nocut)


    def _estimator(self, x):
        options = Options(x, 'q', relaxedcb = True)
        options.spectrum.nsigmas = self.nsigmas
        self.input.histname = self.hpattern % x
        return Spectrum(self.input.read(), options)


    def _probe_spectrum(self, estimator):
        mranges = estimator._mass_ranges()
        results = map(lambda x, y: br.area_and_error(x.mass, *y), estimator.analyzer.masses, mranges)
        ehist = OutputCreator('spectrum', 'Energy spectrum of probe photons; E_{#gamma}, GeV', estimator.analyzer.opt.label)
        ehist = ehist.get_hist(estimator.analyzer.opt.ptedges, results)
        ehist.logy = True
        return ehist


    def eff(self, stop=True, fitfunc=None):
        results = map(self._probe_spectrum, self.cut_and_full)

        for r in results:
            if fitfunc:
                r.fitfunc = fitfunc

        diff = Comparator(stop=stop)
        return diff.compare(results) 