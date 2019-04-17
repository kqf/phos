import click
import ROOT

from drawtools.badmap import badmap
from drawtools.utils import extract_data_lists, draw_and_save, find_similar_in

NOT_RELIABLE = [
    "hCluEXZM3_0",
    "hAsymPtEta",
    "hAsymPtPi0M2",
    "hAsymPtPi0M23",
    "hMassPtCA10_both",
    "hMassPtCA07_both",
    "hMassPtM1",
    "hMassPtM23",
    "hMassPtN6"
]


def compare_visually(hist1, hist2):
    canvas = ROOT.TCanvas("c1", "test",
                          3 * hist1.GetNbinsX() * 8, hist1.GetNbinsY() * 8)
    canvas.Divide(3, 1)
    canvas.cd(1)

    hist1.Draw("colz")

    canvas.cd(2)
    hist2.Draw("colz")
    hist2.SetTitle("Original " + hist2.GetTitle())

    canvas.cd(3)
    hist = hist1.Clone("diff")
    hist.SetTitle(hist1.GetTitle())
    hist.Add(hist2, -1)
    hist.Draw("colz")
    draw_and_save(hist1.GetName(), True, True)
    return hist


def compare_lists_of_histograms(l1, l2, ignore=[], compare=compare_visually):
    if len(l1) != len(l2):
        print "Warning files have different size"

    diffs = []
    for h in l1:
        candidate = find_similar_in(l2, h)
        if not candidate or candidate.GetName() in ignore:
            continue
        diffs.append(compare(h, candidate))
    badmap(diffs)


@click.command()
@click.option('--file1',
              type=click.Path(exists=True),
              help='Path to the first .root file',
              required=True)
@click.option('--file2',
              type=click.Path(exists=True),
              help='Path to the second .root file',
              required=True)
def main(file1, file2):
    ROOT.gROOT.cd()
    ROOT.gStyle.SetOptStat(False)

    hists1 = extract_data_lists(file1)
    hists2 = extract_data_lists(file2)
    compare_lists_of_histograms(hists1, hists2, NOT_RELIABLE, compare_visually)
