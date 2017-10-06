from broot import BROOT as br
from spectrum import Spectrum

class CorrectedYield(object):

    def __init__(self, inpt, options, efficiency):
        super(CorrectedYield, self).__init__()
        self.input = inpt
        self.options = options
        self.efficiency = efficiency


    def evaluate(self):
        scomputor = Spectrum(self.input, self.options)
        spectrum = scomputor.evaluate().spectrum

        corrected_yield = br.ratio(spectrum, self.efficiency)
        corrected_yield.SetTitle(spectrum.GetTitle() + ' corrected for efficiency')
        return br.scalew(corrected_yield)


        