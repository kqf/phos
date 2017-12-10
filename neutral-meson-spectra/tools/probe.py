import os
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

        # IO management
        self.recalculate = False
        self.oname = 'input-data/tof-cut.root'
        self.label = 'tof cut efficiency'


    def eff(self, stop=True, fitfunc=None):
        if self.recalculate:
            return self.efficiency()
        try:
            return self.read_efficiency()
        except IOError:
            return self.efficiency()


    def read_efficiency(self):
        if not os.path.isfile(self.oname):
            raise IOError('No such file: {0}'.format(self.oname))

        infile = ROOT.TFile(self.oname)
        result = infile.GetListOfKeys().At(0).ReadObj()
        result.label = self.label
        return result


    def _estimator(self, x):
        options = Options(x, 'q', ptconf='config/tag-and-probe-tof.json')
        self.input.histname = self.hpattern % x
        return Spectrum(self.input.read(), options)



    def efficiency(self, stop=True, fitfunc=None):
        results = map(lambda x: x.evaluate().spectrum, self.cut_and_full)

        for r in results:
            br.scalew(r)

            if fitfunc:
                r.fitfunc = fitfunc

        diff = Comparator(stop=stop, rrange = (0, 1.01))
        result = diff.compare(results) 

        result.SetTitle(
            'TOF cut efficiency: '
            '#frac{cluster combinations with TOF cut}{all cluster combinations};'
            'E_{#gamma}, GeV; #varepsilon, TOF efficiency'
        )
        result.logy = False
        
        br.io.save(result, self.oname)
        return result
