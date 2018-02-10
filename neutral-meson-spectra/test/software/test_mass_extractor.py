
from spectrum.mass import MassFitter
from spectrum.processing import DataSlicer
from spectrum.options import Options
from spectrum.input import Input
from vault.datavault import DataVault
from spectrum.ptplotter import PtPlotter

import unittest


class UpdatedAnalysis(object):

    def __init__(self, options=Options()):
        super(UpdatedAnalysis, self).__init__()
        self.options = options

    def transform(self, inputs):
        label = inputs.label

        pipeline = [
            inputs,
            # TODO: Clean this part in pipeline
            DataSlicer(self.options.pt, self.options),
            MassFitter(self.options, label)
        ]

        data = None
        for estimator in pipeline:
            data = estimator.transform(data)

        return data

class TestMassFitter(unittest.TestCase):

	def test_fits_the_analysis(self):
		analysis = UpdatedAnalysis()
		masses = analysis.transform(
			Input(DataVault().file("data"), "PhysTender", label='Test')	
		)

		plotter = PtPlotter(masses, analysis.options.output, 'test invarinat mass pipeline')
		plotter.draw()