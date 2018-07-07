#!/usr/bin/python2

import ROOT
import sys
from drawtools.badmap import badmap


def warning(message):
    return "Warning: {}".format(message)


def draw_and_save(name, draw=False, save=True):
    canvas = ROOT.gROOT.FindObject("c1")
    if not canvas:
        return
    canvas.Update()
    if save:
        canvas.SaveAs(name + ".png")
    canvas.Connect("Closed()", "TApplication",
                   ROOT.gApplication, "Terminate()")
    if draw:  # raw_input("Enter some data ...")
        ROOT.gApplication.Run(True)


def hist_cut(h, namecut=lambda x: True):
    res = namecut(h.GetName()) and h.GetEntries() > 0 and h.Integral() > 0
    if not res:
        print "Warning: Empty histogram found: ", h.GetName()
    return res


def get_my_list(filename="AnalysisResults.root"):
    print "Processing %s file:" % filename
    mfile = ROOT.TFile(filename)
    ROOT.gROOT.cd()
    mlist = [key.ReadObj().Clone() for key in mfile.GetListOfKeys()]
    hists = [h for h in mlist if hist_cut(h)]  # Don"t take empty histograms
    return hists


def find_similar_in(lst, ref):
    candidates = [h for h in lst if h.GetName() == ref.GetName()]
    if not candidates:
        msg = "Warning: There is no such histogram {}"
        msg += " in second file or it's empty"
        print msg.format(ref.GetName())
        return None
    if len(candidates) > 1:
        msg = "Warning: you have multiple histograms with the same name!!! Act!!"
        print
    return candidates[0]


def compare_visually(hist1, hist2):
    c1 = ROOT.TCanvas("c1", "test", 3 * hist1.GetNbinsX()
                      * 8, hist1.GetNbinsY() * 8)
    c1.Divide(3, 1)
    c1.cd(1)

    hist1.Draw("colz")

    c1.cd(2)
    hist2.Draw("colz")
    hist2.SetTitle("Original " + hist2.GetTitle())

    c1.cd(3)
    hist = hist1.Clone("diff")
    hist.SetTitle(hist1.GetTitle())
    hist.Add(hist2, -1)
    hist.Draw("colz")
    # draw_and_save(hist1.GetName(), True, True)
    return hist


def compare_lists_of_histograms(l1, l2, ignore=[], compare=compare_visually):
    if len(l1) != len(l2):
        print bcolors.FAIL + "Warning files have different size"

    diffs = []
    for h in l1:
        candidate = find_similar_in(l2, h)
        if not candidate or candidate.GetName() in ignore:
            continue
        diffs.append(compare(h, candidate))
    badmap(diffs)


def compare_histograms():
    ROOT.gROOT.cd()
    ROOT.gStyle.SetOptStat(False)

    if len(sys.argv) < 3:
        print "Usage compare-bmaps.py file1.root file2.root"

    hists1, hists2 = map(get_my_list, sys.argv[1:])
    not_reliable = ["hCluEXZM3_0", "hAsymPtEta", "hAsymPtPi0M2", "hAsymPtPi0M23",
                    "hMassPtCA10_both", "hMassPtCA07_both", "hMassPtM1", "hMassPtM23", "hMassPtN6"]

    compare_lists_of_histograms(hists1, hists2, not_reliable, compare_visually)


def main():
    compare_histograms()


if __name__ == "__main__":
    main()
