import os
import unittest
import progressbar

from spectrum.input import Input, NoMixingInput, read_histogram
from test.software.test_broot import write_histograms


class TestInput(unittest.TestCase):

    def test_reads_single_histogram(self):
        ofilename = 'test_read.root'
        selection = 'testSelection'
        myhist = 'testHistogram'
        histnames = myhist, 'EventCounter'
        original = write_histograms(ofilename, selection, histnames)

        fromfile = read_histogram(ofilename, selection, myhist)

        self.assertIsNotNone(fromfile)
        # We are reading different histograms
        self.assertFalse(fromfile is original[0])

        # And those histograms have the same name
        self.assertEqual(fromfile.GetEntries(), original[0].GetEntries())
        os.remove(ofilename)

    def test_reads_standard_input(self):
        ofilename = 'test_read.root'
        selection = 'testSelection'
        histnames = 'hMassPt', 'hMixMassPt', 'EventCounter'

        original = write_histograms(ofilename, selection, histnames)
        oreal, omixed = original[:-1]
        onevents = original[-1].GetBinContent(2)

        real, mixed = Input(ofilename, selection).read()

        self.assertIsNotNone(real)
        self.assertIsNotNone(mixed)

        # We are reading different histograms
        self.assertFalse(real is oreal)
        self.assertFalse(mixed is omixed)

        # And those histograms have the same name
        self.assertEqual(real.GetEntries(), oreal.GetEntries())
        self.assertEqual(mixed.GetEntries(), omixed.GetEntries())

        self.assertEqual(real.nevents, onevents)
        self.assertEqual(real.nevents, mixed.nevents)
        os.remove(ofilename)

    def test_reads_nomixing_input(self):
        ofilename = 'test_read.root'
        selection = 'testSelection'
        histnames = 'hMassPt', 'EventCounter'

        original = write_histograms(ofilename, selection, histnames)
        oreal, onevents = original[0], original[-1].GetBinContent(2)

        real, mixed = NoMixingInput(ofilename, selection).read()

        self.assertIsNotNone(real)
        self.assertIsNone(mixed)

        # We are reading different histograms
        self.assertFalse(real is oreal)

        # And those histograms have the same name
        self.assertEqual(real.GetEntries(), oreal.GetEntries())

        self.assertEqual(real.nevents, onevents)
        os.remove(ofilename)


class TestInputMemoryPerformance(unittest.TestCase):

    def setUp(self):
        self.infile = 'Pythia-new.root'
        self.sel = 'StudyNonlinOnlyTender'
        self.hname = 'MassPt_%d_%d'
        self.sbins = 11, 11

    @unittest.skip('These tests are only needed to check memory consuptions')
    def test_sequence(self):
        x, y = self.sbins
        bar = progressbar.ProgressBar(maxval=x * y)
        for i in range(x):
            for j in range(y):
                hists = Input(
                    self.infile,
                    self.sel, self.hname % (i, j)).read()
                bar.update(x * i + j)
                self.assertIsNotNone(hists)

    @unittest.skip('These tests are only needed to check memory consuptions')
    def test_copy(self):
        inp = Input(self.infile, self.sel, self.hname % (0, 0))
        raw, mixed = inp.read()

        cache = []
        msize = 11 * 11
        bar = progressbar.ProgressBar()
        for i in bar(range(msize)):
            hists = raw.Clone(), mixed.Clone()
            cache.append(hists)
