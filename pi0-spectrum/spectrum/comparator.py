#!/usr/bin/python2

import ROOT
from sutils import wait 

class bcolors:
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


def hist_cut(h, namecut = lambda x: True): 
    res = namecut( h.GetName() ) and h.GetEntries() > 0 and h.Integral() > 0
    if not res: print bcolors.WARNING +'Warning: Empty histogram found: ', h.GetName(), bcolors.ENDC
    return res

def get_my_list(filename = 'AnalysisResults.root'):
    print 'Processing %s file:' % filename
    mfile = ROOT.TFile(filename)
    ROOT.gROOT.cd() # Without this line your Clones are created inside FILENAME directory. mfile -> local, so this object will when we reach the end of this function. Therefore ROOT this direcotry and all its will be destroyed. 
    mlist = mfile.Data
    # mlist = [key.ReadObj().Clone() for key in mfile.GetListOfKeys()]
    hists = [h for h in mlist if hist_cut(h)] # Don't take empty histograms
    return hists
    


def find_similar_in(lst, ref):
    candidates = [h for h in lst if h.GetName() == ref.GetName() ]
    if not candidates:
        print bcolors.WARNING + 'Warning: There is no such histogram %s%s%s in second file or it\'s empty' % (bcolors.OKGREEN, ref.GetName(), bcolors.WARNING) + bcolors.ENDC
        return None

    if len(candidates) > 1: print bcolors.WARNING + 'Warning: you have multiple histograms with the same name!!! Act!!' + bcolors.ENDC

    return candidates[0]

def isclose(a, b, rel_tol=1e-09):
    return abs(a - b) <= rel_tol

def compare_chi(hist1, hist2):
    percentile = hist1.Chi2Test(hist2)
    if isclose(1., percentile): return #everything is fine
    print bcolors.WARNING + 'Rate of change of %s%s%s is' % (bcolors.OKGREEN, h.GetName(), bcolors.WARNING), percentile, bcolors.ENDC

def compare_visually(hist1, hist2, ci):
    hist1.SetLineColor(ci)
    hist2.SetLineColor(ci + 4)

    hist1.Draw()
    hist2.Draw('same')

    legend = ROOT.TLegend(0.9, 0.4, 1.0, 0.6)
    legend.SetBorderSize(0)
    legend.SetFillStyle(0)
    legend.SetTextSize(0.04)
    legend.AddEntry(hist1, hist1.label)
    legend.AddEntry(hist2, hist2.label)
    legend.Draw('same')

    if 'spectr' in hist1.GetName():
        ROOT.gPad.SetLogy()

    wait(hist1.GetName(), True)


class Comparator(object):
    def __init__(self, ):
        super(Comparator, self).__init__()
        self.ci, self.colors = self.define_colors()

    def compare_lists_of_histograms(self, l1, l2, ignore = [], compare = compare_visually):
        if len(l1) != len(l2): 
            print bcolors.FAIL + 'Warning files have different size' + bcolors.ENDC

        for h in l1: 
            candidate = find_similar_in(l2, h)
            if not candidate or candidate.GetName() in ignore: continue
            compare(h, candidate, self.ci)

        print "That's it!! Your computation is done"

    def define_colors(self, ci = 1000):
        colors = [ (219 , 86  , 178), (160 , 86  , 219), (86  , 111 , 219), (86  , 211 , 219), (86  , 219 , 127),  (219 , 194 , 86), (219 , 94 , 86)]
        rcolors = [[b / 255. for b in c] for c in colors]
        rcolors = [ROOT.TColor(ci + i, *color) for i, color in enumerate(rcolors)]
        return ci, rcolors

def compare_histograms():
    ROOT.gROOT.cd()
    ROOT.gStyle.SetOptStat(False)

    hists1 = get_my_list('testB.root')
    hists2 = get_my_list('AnalysisResults.root')

    not_reliable = [""]

    diff = Comparator()
    diff.compare_lists_of_histograms(hists1, hists2, not_reliable, compare_visually)



def main():
    compare_histograms()

if __name__ == '__main__':
    main()
