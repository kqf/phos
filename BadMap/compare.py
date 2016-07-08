#!/usr/bin/python2

import ROOT

class bcolors:
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

def draw_and_save(name, draw=False, save=True):
    canvas = ROOT.gROOT.FindObject('c1')
    if not canvas: return
    canvas.Update()
    if save: canvas.SaveAs(name + '.png')
    canvas.Connect("Closed()", "TApplication", ROOT.gApplication, "Terminate()")
    if draw:# raw_input('Enter some data ...')
        ROOT.gApplication.Run(True)

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

def compare_visually(hist1, hist2):
    hist1.SetLineColor(37)
    hist2.SetLineColor(48)

    hist1.Draw()
    hist2.Draw('same')

    draw_and_save(hist1.GetName(), True, True)


class Comparator(object):
    def __init__(self, ):
        super(Comparator, self).__init__()
        
    def compare_lists_of_histograms(self, l1, l2, ignore = [], compare = compare_chi):
        if len(l1) != len(l2): 
            print bcolors.FAIL + 'Warning files have different size' + bcolors.ENDC

        for h in l1: 
            candidate = find_similar_in(l2, h)
            if not candidate or candidate.GetName() in ignore: continue
            compare(h, candidate)

        print "That's it!! Your computation is done"

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
