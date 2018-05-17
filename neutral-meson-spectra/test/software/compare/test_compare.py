import unittest
import spectrum.comparator as cmpr
from particles import Particles


class TestComparator(unittest.TestCase, Particles):

    def setUp(self):
        self.data, self.stop = self.config()

    def testCompareMultiple(self):
        diff = cmpr.Comparator(stop=self.stop)
        self.data[0].SetTitle('Testing compare set of histograms: explicit')
        diff.compare_set_of_histograms(zip(*[self.data]))

        self.data[0].SetTitle('Testing compare set of histograms: "compare"')
        diff = cmpr.Comparator(stop=self.stop)
        diff.compare(self.data)

    def testPriority(self):
        diff = cmpr.Comparator(stop=self.stop)

        for h in self.data:
            h.SetTitle('Checking priority of the histograms')

        data = self.data[0].Clone()
        data.label = 'distorted'

        # Distort the data intentionally
        data.SetBinContent(2, data.GetBinContent(2) * 100)
        data.SetBinContent(55, -1 * data.GetBinContent(55))

        # Without priority
        diff.compare(self.data[0], data)

        data.priority = 0
        self.data[0].priority = 999

        # With priority
        diff.compare(self.data[0], data)

    # @unittest.skip('test')
    def testSuccesive(self):
        """
            Explanation:
                This is needed to check if behaviour changes after double usage of a comparator.
                Also this test assures that comparison "A" and "B" and "B" and "A" work as needed.
        """

        diff = cmpr.Comparator(stop=self.stop)

        self.data[2].SetTitle('Checking if compare is able to redraw' +
                              'same images properly, Check 1')
        diff.compare(self.data[2], self.data[1])

        self.data[2].SetTitle('Checking if compare is able to redraw' +
                              'same images properly, Check 2')
        diff.compare(self.data[2], self.data[1])

        self.data[1].SetTitle('Checking if compare is able to redraw' +
                              'same images properly: reverse order of histograms')
        diff.compare(self.data[1], self.data[2])
