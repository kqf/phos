#!/usr/bin/python2

import json
import ROOT

from vis import VisHub

# TODO: Separate multiple visualisator from double
#       It's possible to arrange: compare_visually calls draw, and draw double
#       ivoke right function from the Comparator class, Replece unnecesaary ifs

class Comparator(object):
    ci, colors = define_colors()

    def __init__(self, size = (1, 1), rrange = None, crange = None, stop = True, oname = ''):
        super(Comparator, self).__init__()
        self.vi = VisHub(size, rrange, crange, stop, oname)


    def compare(self, *args):
        contains_objs = lambda x: all(not '__iter__' in dir(i) for i in x)

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
        if len(args) == 2 and  all(map(contains_objs, args)):
            return self.compare_set_of_histograms(args)

        # Handle sets of histograms
        #
        if len(args) == 1 and all(map(contains_objs, args[0])):
            return self.compare_set_of_histograms(args[0])

        assert False, "Can't deduce what are you trying to with these arguments:\n {}".format(args)


    def compare_multiple_ratios(self, hists, baselines, comparef = None):
        if not comparef:
            comparef = self.vi.compare_visually

        def ratio(a, b):
            h = a.Clone(a.GetName() + '_ratio')
            # Here we assume that a, b have the same lables
            h.label = a.label
            h.Divide(b)
            ytitle = lambda x: x.GetYaxis().GetTitle()
            h.SetTitle(a.GetTitle() + ' / ' + b.GetTitle())
            h.GetYaxis().SetTitle(ytitle(a) +  ' / ' + ytitle(b))
            return h

        comparef(map(ratio, hists, baselines), self.ci)



    def compare_ratios(self, hists, baseline, comparef = None, logy = False):
        if not comparef:
            comparef = self.vi.compare_visually

        def ratio(a):
            h = a.Clone(a.GetName() + '_ratio')
            h.label = a.label + '/' + baseline.label
            h.Divide(baseline)
            if logy: h.logy = logy
            return h

        comparef(map(ratio, hists), self.ci)


    def compare_set_of_histograms(self, l, comparef = None):
        if not comparef:
            comparef = self.vi.compare_visually

        result = [comparef(hists, self.ci) for hists in zip(*l)]
        return result if len(result) > 1 else result[0]

    @staticmethod
    def define_colors(ci = 1000):
        with open("config/colors.json") as f:
            conf = json.load(f)
            
        colors = conf["colors"]
        rcolors = [[b / 255. for b in c] for c in colors]
        rcolors = [ROOT.TColor(ci + i, *color) for i, color in enumerate(rcolors)]
        return ci, rcolors

def main():
    print "Use:\n\t... \n\tcmp = Comparator((0.5, 2))\n\t...\n\nto comparef lists of histograms."

if __name__ == '__main__':
    main()
