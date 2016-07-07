#!/usr/bin/python

import ROOT
import sys
import subprocess

def get_my_list(filename = 'AnalysisResults.root'):
    print 'Processing %s file:' % filename
    mfile = ROOT.TFile(filename)
    mfile.ls()
    mlist = [k.ReadObj() for k in mfile.GetListOfKeys()]
    return mlist
    
def compare_histograms():
    ROOT.gROOT.cd()
    name = sys.argv[1] if len(sys.argv) > 1 else 'AnalysisResults.root'
    selections = get_my_list(name)
    for selection in  selections:
        print selection.GetName(), 'N(hists):' ,selection.GetEntries(), selection.GetTitle()
        for h in selection:
        	print h.GetName(), h.GetTitle(), h.GetEntries()



def main():
    compare_histograms()

if __name__ == '__main__':
    main()
