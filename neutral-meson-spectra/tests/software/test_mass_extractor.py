import unittest
import pytest

from spectrum.processing import DataSlicer
from spectrum.processing import MassFitter
from spectrum.output import AnalysisOutput
from spectrum.pipeline import TransformerBase
from spectrum.pipeline import Pipeline
from spectrum.processing import InvariantMassExtractor

from spectrum.options import Options
from vault.datavault import DataVault


class UpdatedAnalysis(TransformerBase):

    def __init__(self, options=Options()):
        super(UpdatedAnalysis, self).__init__()
        self.options = options
        self.pipeline = Pipeline([
            ('data_slicer', DataSlicer(self.options.pt)),
            ('mass_extractor', InvariantMassExtractor(self.options.invmass)),
            ('mass_fitter', MassFitter(self.options.invmass.use_mixed))
        ])


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
        self.assertGreater(len(masses), 0)

    @pytest.mark.onlylocal
    def test_fits_the_analysis(self):
        self.run_analysis(mixed=False)

    @pytest.mark.onlylocal
    def test_fits_the_analysis_mixed(self):
        self.run_analysis(mixed=True)
