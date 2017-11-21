from sutils import wait
from sutils import gcanvas
from comparator import Comparator
from broot import BROOT as br

import ROOT

import os.path


# TODO: Merge with efficiency ???


class Nonlinearity(object):
    def __init__(self, data, mc, function, rrange = (0.90, 1.08), mcname = ''):
        super(Nonlinearity, self).__init__()
        self.data = data
        self.mc = mc
        self.function = function
        self.rrange = rrange
        self.nonlinearity_file = 'nonlinearity-{0}.root'.format(mcname)

    def _ratio(self, fname):
        self.data = self._extract_mass(self.data)
        self.mc = self._extract_mass(self.mc)
        self.data.fitfunc = self.function
        diff = Comparator()
        ratio = diff.compare(self.data, self.mc)

        br.io.save(ratio, fname)
        return ratio

    # NB: This way we can pass both mass,
    #     and estimators to Nonlinearity constructor
    def _extract_mass(self, estimator):
        try:
            return estimator.evaluate().mass
        except AttributeError:
            return estimator

    def _read(self, fname):
        if not os.path.isfile(fname):
            raise IOError('No such file: {0}'.format(fname))

        infile = ROOT.TFile(fname)
        return infile.GetListOfKeys().At(0).ReadObj()

    def ratio(self, filename):
        try:
            return self._read(filename)
        except IOError:
            return self._ratio(filename)

    def evaluate_parameters(self):
        canvas = gcanvas()
        a, b = self.rrange

        ratio = self.ratio(self.nonlinearity_file)
        ratio.SetAxisRange(a, b, 'Y')
        ratio.Fit(self.function)
        ratio.Draw()

        parameters = map(self.function.GetParameter, range(self.function.GetNpar()))
        print 'Nonlinearity parameters: {}'.format(parameters)
        wait(ratio.GetName())