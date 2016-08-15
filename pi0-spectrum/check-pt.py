#!/usr/bin/python

import ROOT
import numpy as np
from CrystallBall import Fit

ROOT.TH1.AddDirectory(False)

def draw_and_save(name, draw=True, save=False):
    canvas = ROOT.gROOT.FindObject('c1')
    if not canvas: return
    canvas.Update()
    if save: canvas.SaveAs('results/' + name + '.pdf')
    canvas.Connect("Closed()", "TApplication", ROOT.gApplication, "Terminate()")
    if draw: ROOT.gApplication.Run(True)


def read_hists(fname='AnalysisResults.root', name = 'test'):
    mfile = ROOT.TFile(fname)
    mfile.ls()
    mlist = mfile.Data
    mlist.ls()
    mlist = mfile.PhysTheBest
    mlist.ls()
    mlist = [k for k in mlist if name in k.GetName()]
    return mlist

def extract_inv_mass(data, lower_bound):
    yaxis = data.GetYaxis()
    lower_bin, upper_bin = yaxis.FindBin(lower_bound), yaxis.GetLast()

    module = data.GetName()[-1]
    newname = 'mass_sm' + module + '_pt_%3g' % (lower_bound * 1000)
    ncells = 2 if 'N3' in data.GetName() else 0
    ncells = 'N_{cell} > '  + str(ncells)
    newtitle = ' p_{T} > %3.g GeV/c ' % lower_bound + ncells

    hist = data.ProjectionX(newname, lower_bin, upper_bin)
    hist.SetTitle(newtitle)
    hist.label = 'SM' + module 
    hist.GetXaxis().SetTitle('M_{#gamma#gamma}, GeV/c^{2}')

    hist.Draw()
    hist.Rebin(2)
    # draw_and_save('test')
    return hist


import compare as cmpr

def main():
    pt_ranges = [2, 5, 8, 10]
    old_poor = read_hists('LHC16g.root', 'hMassPtSM')
    old_poor = [ map(lambda x: extract_inv_mass(x, pt), old_poor) for pt in pt_ranges]

    for hists, pt in zip(old_poor, pt_ranges):
        legend = ROOT.TLegend(0.5, 0.5, 0.8, 0.8)
        legend.SetBorderSize(0)
        legend.SetFillStyle(0)
        diff = cmpr.Comparator(legend = legend, normalize = True, title = ' p_{T} > %3.g GeV/c' % pt)
        hists = hists[0:3]
        diff.compare_lists_of_histograms(hists[::-1])


if __name__ == '__main__':
    main()