from broot import BROOT as br
from spectrum import Spectrum
from .input import Input
from options import Options
from efficiency import Efficiency

class CorrectedYield(object):

    def __init__(self, inpt, options, efficiency):
        super(CorrectedYield, self).__init__()
        self.input = inpt
        self.options = options
        self.efficiency = efficiency


    def evaluate(self):
        scomputor = Spectrum(self.input, self.options)
        # TODO: Add loggs here
        spectrum = scomputor.evaluate().spectrum

        corrected_yield = br.ratio(spectrum, self.efficiency)
        corrected_yield.SetTitle(spectrum.GetTitle() + ' corrected for efficiency')
        return br.scalew(corrected_yield)

    @classmethod
    def create_evaluate(klass, infile = 'LHC16.root', sel = 'PhysOnlyTender', 
                        effile = 'Pythia-LHC16-a5', effhist = 'hPt_#pi^{0}_primary_'):

       inp, opt = Input(infile, sel, label='data'), Options('q')
       eff = Efficiency(effhist, 'eff', effile).eff()
       cy_estimator = klass(inp, opt, eff)

       corrected_spectrum = cy_estimator.evaluate()
       return corrected_spectrum
