#!/usr/bin/python2

import ROOT
from sutils import wait, get_canvas

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

def preare_ratio_plot(hists):
    c1 = get_canvas()
    if len(hists) != 2: return c1, c1, c1
    pad1 = ROOT.TPad("pad1","main plot", 0, 0.3, 1, 1);
    pad1.SetBottomMargin(0);
    pad1.Draw()
    c1.cd()
    pad2 = ROOT.TPad("pad2","ratio", 0, 0, 1, 0.3);
    pad2.SetTopMargin(0);
    pad2.Draw();
    pad2.SetTickx()
    pad2.SetTicky()
    return c1, pad1, pad2

def draw_ratio(hists):
    if len(hists) != 2: return
    a, b = hists
    ratio = a.Clone('ratio' + a.GetName())
    ratio.GetYaxis().SetTitleSize(0.06)
    ratio.GetYaxis().SetTitleOffset(0.3)
    ratio.GetYaxis().CenterTitle(True)
    ratio.GetXaxis().SetTitleSize(0.06)
    ratio.GetXaxis().SetTitleOffset(0.7) 
    ratio.GetXaxis().SetLabelSize(0.08) 

    ratio.Divide(b)
    label = a.label + ' / ' + b.label
    ratio.SetTitle('')
    ratio.GetYaxis().SetTitle(label)
    ratio.Draw()
    ROOT.gPad.SetGridy()
    return ratio 

def compare_visually(hists, ci):
    canvas, mainpad, ratio = preare_ratio_plot(hists)

    legend = ROOT.TLegend(0.8, 0.4, 0.9, 0.6)
    legend.SetBorderSize(0)
    # legend.SetFillStyle(0)
    legend.SetTextSize(0.04)

    mainpad.cd()
    hists[0].DrawCopy()
    for i, h in enumerate(hists): 
        h.SetLineColor(ci + i)
        h.DrawCopy('same')
        h.SetFillColor(ci + i)
        h.SetMarkerStyle(21)
        h.SetMarkerColor(ci + i)
        legend.AddEntry(h, h.label)

    legend.Draw('same')

    if 'spectr' in hists[0].GetName() or 'chi' in hists[0].GetName() :
        ROOT.gPad.SetLogy()
    ROOT.gStyle.SetOptStat(0)
    ROOT.gPad.SetTickx()
    ROOT.gPad.SetTicky() 

    ratio.cd()
    ratio = draw_ratio(hists)

    # ctrl+alt+f4 closes enire canvas not just a pad.
    canvas.cd()
    wait(hists[0].GetName(), True)


class Comparator(object):
    def __init__(self, ):
        super(Comparator, self).__init__()
        self.ci, self.colors = self.define_colors()

    def compare_set_of_histograms(self, l, compare = compare_visually):
        for hists in zip(*l):
            compare(hists, self.ci)

    def compare_lists_of_histograms(self, l1, l2, ignore = [], compare = compare_visually):
        if len(l1) != len(l2): 
            print bcolors.FAIL + 'Warning files have different size' + bcolors.ENDC

        for h in l1: 
            candidate = find_similar_in(l2, h)
            if not candidate or candidate.GetName() in ignore: continue
            compare(h, candidate, self.ci)

        print "That's it!! Your computation is done"

    def define_colors(self, ci = 1000):
        colors = [ (219 , 86  , 178), (160 , 86  , 219), (86  , 111 , 219), (86  , 211 , 219), (86  , 219 , 127),  (219 , 194 , 86), (219 , 94 , 86)][::-1]
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
