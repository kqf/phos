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
    def __init__(self,
        dataset,
        cut_nocut=('TOF', 'All'),
        selection='TagAndProbleTOFOnlyTender',
        hpattern='MassEnergy%s_SM0'
    ):
        super(TagAndProbe, self).__init__()

        # Create inputs for cut and nocut hists
        inputs = map(
            self._input_creator(
                dataset,
                selection,
                hpattern
            ),
            cut_nocut
        )

        # Create estimators for the different datasets
        self.cut_and_full = map(
            self._estimator, 
            inputs
        )

        # IO management
        self.recalculate = False
        self.oname = 'input-data/tof-cut' + \
                      inputs[0].filename + \
                      (hpattern % '') + '.root'
        self.label = 'tof cut efficiency'


    def _estimator(self, inputs):
        options = Options(ptrange='config/tag-and-probe-tof.json')
        return Spectrum(inputs, options)


    def _input_creator(self, data, selection, hpattern):
        function = lambda x: Input(
            data,
            selection,
            hpattern % x,
            label=x
        )
        return function


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
