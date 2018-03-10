
from spectrum.processing import DataSlicer
from spectrum.processing import MassFitter

from spectrum.options import Options
from spectrum.input import Input
from vault.datavault import DataVault

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

    def run_analysis(self, mixed):
        options = Options()
        options.pt.use_mixed = mixed
        analysis = UpdatedAnalysis(options)
        masses = analysis.transform(
            Input(DataVault().file("data"), "PhysTender", label='Test')
        )

    def test_fits_the_analysis(self):
        self.run_analysis(mixed=False)

    def test_fits_the_analysis_mixed(self):
        self.run_analysis(mixed=True)




