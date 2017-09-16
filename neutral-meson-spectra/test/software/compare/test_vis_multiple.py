import unittest

import spectrum.comparator as cmpr
import spectrum.vis as vi

from particles import Particles

class TestMultipleVisualizer(unittest.TestCase, Particles):
    """
        Develop multiple visualizer
    """

    def setUp(self):
        self.data, self.stop = self.config()


    # @unittest.skip('')
    def test_draws_multiple_plots(self):
        vis = vi.VisHub((1, 1), (), (), True, '')

        self.data[0].SetTitle('Test ViHub: Testing MultipleVisualizer')
        vis.compare_visually(self.data, 1)

        
        self.data[0].SetTitle('Test VisHub: MultipleVisualizer')
        vis.compare_visually(self.data[0:2], 1)


        self.data[0].SetTitle('Test VisHub: Single Visualizer')
        vis.compare_visually(self.data[0:2], 1)

