import unittest

import spectrum.comparator as cmpr

from particles import Particles

class TestMultipleVisualizer(unittest.TestCase, Particles):
    """
        Develop multiple visualizer
    """

    def setUp(self):
        self.data, self.stop = self.config()


    @unittest.skip('')
    def test_draws_multiple_plots(self):
        # TODO: Separate further double plot and multiple plot graphs
        diff = cmpr.Comparator()
        diff.vi = cmpr.MultipleVisualizer((1, 1), None, None, True, '')

        self.data[0].SetTitle('Testing MultipleVisualizer')
        diff.compare(self.data)

