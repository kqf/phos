import click
import ROOT

from drawtools.badmap import badmap
from drawtools.utils import compare_lists_of_histograms, draw_and_save
from drawtools.utils import extract_data_lists

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


def compare_visually(hist1, hist2, scale=8, aspect_ratio=3):
    canvas = ROOT.TCanvas(
        "c1", "canvas",
        hist1.GetNbinsX() * scale * aspect_ratio,
        hist1.GetNbinsY() * scale)
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


@click.command()
@click.option("--file1", type=click.Path(exists=True), required=True)
@click.option("--file2", type=click.Path(exists=True), required=True)
def main(file1, file2):
    ROOT.gROOT.cd()
    ROOT.gStyle.SetOptStat(False)

    hists1 = extract_data_lists(file1)
    hists2 = extract_data_lists(file2)
    diff = compare_lists_of_histograms(
        hists1, hists2,
        NOT_RELIABLE, compare_visually)
    badmap(diff)
