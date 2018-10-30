
import sys
import unittest
import pytest

from spectrum.sutils import wait
from spectrum.options import Options
from spectrum.invariantmass import InvariantMass
from spectrum.processing import DataSlicer, MassFitter, RangeEstimator
from spectrum.processing import InvariantMassExtractor
from spectrum.output import AnalysisOutput
from spectrum.pipeline import Pipeline

from vault.datavault import DataVault


class TestInvariantMass(unittest.TestCase):

    def setUp(self):
        self.wait = 'discover' not in sys.argv
        self.wait = self.wait and 'pytest' not in sys.argv[0]
        self.input = DataVault().input(
            "data",
            "stable",
            label='testinvmass'
        )
        self.particles = {
            'pi0': (8, 9),
            'eta': (0.8, 1.4)
        }

    def draw(self, particle, func, title):
        bin, nrebin = self.particles[particle]
        mass = InvariantMass(self.input, bin, nrebin,
                             Options(particle=particle))
        mass.extract_data()
        # NB: Add this to be able to see the significance
        mass.area_error = 10, 0.05
        func(mass)
        wait('test-inmass-%s-' % particle + title, self.wait, True)

    def draw_multiple(self, particle):
        option = Options(particle=particle)

        pipeline = Pipeline([
            ('slice', DataSlicer(option.pt)),
            ('extract', InvariantMassExtractor(option.invmass)),
            ('fit', MassFitter(option.invmass.use_mixed)),
            ("ranges", RangeEstimator(option.spectrum)),
        ])

        loggs = AnalysisOutput("test-multirage-plotter", particle)
        masses = pipeline.transform(self.input, loggs)
        loggs.update({"invariant-masses": masses})
        loggs.plot(stop=self.wait)

    # @unittest.skip('')
    @pytest.mark.onlylocal
    def test_multiple_plots(self):
        for p in self.particles:
            self.draw_multiple(p)
