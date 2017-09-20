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


    def test_vis_hub(self):
        vishub = vi.VisHub((1, 1), (), (), self.stop, '')

        self.data[0].SetTitle('Test ViHub: Testing MultipleVisualizer')
        vishub.compare_visually(self.data, 1)

        
        self.data[0].SetTitle('Test VisHub: MultipleVisualizer')
        vishub.compare_visually(self.data[0:2], 1)


        self.data[0].SetTitle('Test VisHub: Single Visualizer')
        vishub.compare_visually([self.data[0]], 1)


    def test_draws_multiple_plots(self):
        vishub = vi.VisHub((1, 1), (), (), self.stop, '')
        vis = vishub._regular


        self.data[0].SetTitle('Test VisMultiple: Testing MultipleVisualizer')
        vis.compare_visually(self.data, 1)

        
        self.data[0].SetTitle('Test VisMultiple: MultipleVisualizer')
        vis.compare_visually(self.data[0:2], 1)

        self.data[0].SetTitle('Test VisMultiple: Test Single')
        vis.compare_visually([self.data[0]], 1)


    def test_handles_double_plots(self):
        vishub = vi.VisHub((1, 1), (), (), self.stop, '')
        vis = vishub._double

        self.assertRaises(ValueError, vis.compare_visually, self.data, 1)

        
        self.data[0].SetTitle('Test DoubleVis: Visualize two plots')
        vis.compare_visually(self.data[0:2], 1)
