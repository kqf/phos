#!/usr/bin/python

import ROOT
import subprocess
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def merge_files(files, ofile, directory='pictures/'):
    ifiles  = '.png '.join(files) + '.png'
    command = 'convert ' + ifiles + ' -append ' + ofile + '.png'
    subprocess.Popen('cd %s; pwd; ' % directory + command, shell=True).wait()
    command = 'rm ' + ifiles
    subprocess.Popen('cd %s; ' % directory + command, shell=True)
    # subprocess.Popen('cd %s; ' % directory + command, shell=True)


def save_histogram(h, filename='default'):
    ofile = ROOT.TFile.Open(filename + '.root', 'recreate')
    h.Write()
    ofile.Write()


def draw_and_save(name, draw=False, save=True):
    canvas = ROOT.gROOT.FindObject('c1')
    if not canvas: return
    canvas.Update()
    if save: canvas.SaveAs('pictures/' + name + '.png')
    canvas.Connect("Closed()", "TApplication", ROOT.gApplication, "Terminate()")
    if draw: raw_input('Enter some data ...')
        # ROOT.gApplication.Run(True)


def get_my_list(filename):
    print 'Processing %s file:' % filename
    mfile = ROOT.TFile(filename)
    mlist = mfile.PhysNonlinTender
    return mlist
    
def hist_cut(h, namecut = lambda x: True): 
    res = namecut( h.GetName() ) and h.GetEntries() > 0 and h.Integral() > 0
    if not res: print bcolors.WARNING +'Warning: Empty histogram found: ', h.GetName(), bcolors.ENDC
    return res

def find_similar_in(lst, ref):
    candidates = [h for h in lst if h.GetName() == ref.GetName() ]
    if not candidates:
        print bcolors.WARNING + 'Warning: There is no such histogram %s%s%s in second file or it\'s empty' % (bcolors.OKGREEN, ref.GetName(), bcolors.WARNING) + bcolors.ENDC
        return None

    if len(candidates) > 1: print bcolors.WARNING + 'Warning: you have multiple histograms with the same name!!! Act!!' + bcolors.ENDC

    return candidates[0]

def isclose(a, b, rel_tol=1e-09):
    return abs(a - b) <= rel_tol

def compare_lists_of_histograms(l1, l2, ignore = []):
    if len(l1) != len(l2): 
        print bcolors.FAIL + 'Warning files have different size' + bcolors.ENDC
        l1, l2 = max(l1, l2, key=len), min(l1, l2, key=len)

    for h in l1: 
        candidate = find_similar_in(l2, h)
        if not candidate: continue
        percentile = h.Chi2Test(candidate)
        if not isclose(1., percentile) and not h.GetName() in ignore: 
            print bcolors.WARNING + 'Rate of change of %s%s%s is' % (bcolors.OKGREEN, h.GetName(), bcolors.WARNING), percentile, bcolors.ENDC
        else:
            print '{0}The histograms {1} are identical {2}'.format(bcolors.OKGREEN, h.GetName(), bcolors.ENDC)


def compare_histograms():
    ROOT.gROOT.cd()
    mlist1 = get_my_list('reference.root')

    my_hists = (h for h in mlist1 if hist_cut(h) )
    hists1 = list(my_hists)

    import sys
    mlist2 = get_my_list(sys.argv[1])
    my_hists = (h for h in mlist2 if hist_cut(h) )
    hists2 = list(my_hists)

    not_reliable = ["hCluEXZM3_0", "hAsymPtEta", "hAsymPtPi0M2", "hAsymPtPi0M23", "hMassPtCA10_both", "hMassPtCA07_both", "hMassPtM1", "hMassPtM23", "hMassPtN6"]
    compare_lists_of_histograms(hists1, hists2, not_reliable)



def main():
    compare_histograms()

if __name__ == '__main__':
    main()
