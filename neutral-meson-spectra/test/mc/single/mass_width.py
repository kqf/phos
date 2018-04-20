from spectrum.spectrum import Spectrum, CompositeSpectrum
from spectrum.input import Input
from spectrum.options import Options
from spectrum.broot import BROOT as br
import spectrum.comparator as cmpr


class MassWidthVerification(object):

    def spectrum_shape(self, shape_input):
        spectrum_estimator = CompositeSpectrum(self.shape_inputs)
        spmc = spectrum_estimator.evaluate()
        br.scalew(spmc.spectrum, 1. / spmc.spectrum.Integral())
        spmc.spectrum.label = 'mc'

        dinp, dopt = Input(
            'LHC16',
            'PhysOnlyTender',
            label='data'), Options('d')

        data = Spectrum(dinp, dopt).evaluate()
        br.scalew(data.spectrum, 1. / data.spectrum.Integral())

        diff = cmpr.Comparator()
        diff.compare(data.spectrum, spmc.spectrum)
