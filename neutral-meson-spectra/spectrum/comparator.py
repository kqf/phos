#!/usr/bin/python2

from vis import VisHub
from broot import BROOT as br


class Comparator(object):

    ci, colors = br.define_colors()

    def __init__(self, size=(1, 1), rrange=(), crange=(),
                 stop=True, oname='', labels=None):
        super(Comparator, self).__init__()
        self.vi = VisHub(size, rrange, crange, stop, oname, labels)

    def compare(self, *args):
        def contains_objs(x):
            return all('__iter__' not in dir(i) for i in x)

        # Halndle coma separated histograms
        #
        if contains_objs(args):
            return self.vi.compare_visually(args, self.ci)

        # Halndle single list of histograms
        #
        if len(args) == 1 and contains_objs(args[0]):
            return self.vi.compare_visually(args[0], self.ci)

        # Halndle two lists of histograms
        #
        if len(args) == 2 and all(map(contains_objs, args)):
            return self.compare_set_of_histograms(args)

        # Handle sets of histograms
        #
        if len(args) == 1 and all(map(contains_objs, args[0])):
            return self.compare_set_of_histograms(args[0])

        message = "Can't deduce what are you" \
            " trying to do with these arguments:\n {}".format(args)
        assert False, message

    def compare_multiple_ratios(self, hists, baselines, comparef=None):
        if not comparef:
            comparef = self.vi.compare_visually
        comparef(map(br.ratio, hists, baselines), self.ci)

    def compare_ratios(self, hists, baseline, comparef=None, logy=False):
        if not comparef:
            comparef = self.vi.compare_visually

        def ratio(x):
            return br.ratio(x, baseline)
        comparef(map(ratio, hists), self.ci)

    def compare_set_of_histograms(self, l, comparef=None):
        if not comparef:
            comparef = self.vi.compare_visually

        result = [comparef(hists, self.ci) for hists in zip(*l)]
        return result if len(result) > 1 else result[0]
