#!/usr/bin/python2

import ROOT
import sys

all_palettes  = [51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109]

def badmap(hists, c1 = None):
    # ROOT.gStyle.SetPalette(i)
    if not c1:
        c1 = ROOT.TCanvas('c1', 'c1', 128 * 5, 96 * 5);
        c1.Divide(2, 2);

    for i, sm in enumerate(hists):
        pad = c1.cd(i + 1);
        # print sm.label, sm.GetEntries()
        sm.Draw(sm.option)

    c1.Update()
    c1.SaveAs(hists[0].GetName() + '.pdf')

def main():
    assert len(sys.argv) == 2, "Usage ./badmap.py file.root"
    infile = ROOT.TFile(sys.argv[1])
    hists = [k.ReadObj() for k in infile.GetListOfKeys()]

    badmap(hists)
    # for i in all_palettes: badmap(hists, 'c', i)

if __name__ == '__main__':
    main()