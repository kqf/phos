
from spectrum.processing import DataSlicer
from spectrum.processing import MassFitter
from spectrum.output import AnalysisOutput
from spectrum.transformer import TransformerBase
from spectrum.pipeline import Pipeline

from spectrum.options import Options
from spectrum.input import Input
from vault.datavault import DataVault

import unittest


class UpdatedAnalysis(TransformerBase):

    def __init__(self, options=Options()):
        super(UpdatedAnalysis, self).__init__()
        self.options = options
        self.pipeline = Pipeline([
            ('data_slicer', DataSlicer(self.options.pt)),
            ('mass_fitter', MassFitter(self.options.invmass))
        ])

    # def transform(self, inputs, loggs):
    #     label = inputs.label

    #     pipeline = [
    #         # TODO: Clean this part in pipeline
    #         DataSlicer(self.options.pt),
    #         MassFitter(self.options.invmass)
    #     ]

    #     for estimator in pipeline:
    #         data = estimator.transform(inputs, loggs)

    #     return data


class TestMassFitter(unittest.TestCase):

    def run_analysis(self, mixed):
        options = Options()
        options.pt.use_mixed = mixed
        analysis = UpdatedAnalysis(options)
        loggs = AnalysisOutput("test_mass_fitter")
        masses = analysis.transform(
            DataVault().input("data", label='Test'),
            loggs

        )

    def test_fits_the_analysis(self):
        self.run_analysis(mixed=False)

    def test_fits_the_analysis_mixed(self):
        self.run_analysis(mixed=True)




