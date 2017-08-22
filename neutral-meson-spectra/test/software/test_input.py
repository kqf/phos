from spectrum.input import Input, TimecutInput, read_histogram

import ROOT
import os.path
import unittest
import progressbar

class TestInput(unittest.TestCase):

    def setUp(self):
        self.infile = 'Pythia-new.root'
        self.sel = 'StudyNonlinOnlyTender'
        self.hname = 'MassPt_%d_%d'
        self.sbins = 11, 11

    # @unittest.skip('This test should be skipped unless\
     # it will be clear how do reduce memory usage')
    def test_sequence(self):
        x, y = self.sbins
        bar = progressbar.ProgressBar(maxval = x * y) 
        for i in range(x):
            for j in range(y):
                hists = Input(self.infile, self.sel, self.hname % (i, j)).read()
                bar.update(x * i + j)


    @unittest.skip('')
    def test_copy(self):
        """
            This one is needed to check memory usage
        """
        inp = Input(self.infile, self.sel, self.hname % (0, 0))
        raw, mixed = inp.read()

        cache = []
        msize = 11 * 11
        bar = progressbar.ProgressBar() 
        for i in bar(range(msize)):
            hists = raw.Clone(), mixed.Clone()
            cache.append(hists)
            raw_input('Press enter')






