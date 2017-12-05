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
    def __init__(self, sinput, cut_nocut = ('TOF', 'All')):
        super(TagAndProbe, self).__init__()
        self.hpattern = sinput.histname
        self.input = sinput
        self.cut_and_full = map(self._estimator, cut_nocut)


    def _estimator(self, x):
        options = Options(x, 'q', ptconf='config/tag-and-probe-tof.json')
        self.input.histname = self.hpattern % x
        return Spectrum(self.input.read(), options)



    def eff(self, stop=True, fitfunc=None):
        results = map(lambda x: x.evaluate().spectrum, self.cut_and_full)

        for r in results:

            r.SetTitle('Energy spectrum of probe photons; E_{#gamma}, GeV')
            br.scalew(r)

            if fitfunc:
                r.fitfunc = fitfunc

        diff = Comparator(stop=stop, rrange = (0, 1.01))
        return diff.compare(results) 