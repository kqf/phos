from __future__ import print_function
import ROOT
import click
from drawtools.utils import extract_data_lists
from drawtools.utils import error, compare_lists_of_histograms


def compare_bin_by_bin(hist1, hist2):
    i1, i2 = hist1.Integral(), hist2.Integral()
    if int(i1 - i2) != 0:
        return error(
            "The histograms {} are different. Int1 - Int2 = {}".format(
                hist1.GetName(), str(i1 - i2)))

    def f(x):
        return [x.GetBinContent(i + 1) for i in range(x.GetNbinsX())]
    if not f(hist1) == [i for i in f(hist2)]:
        error("Some bins are different in " + hist1.GetName())
    print("Histograms are".format(hist1.GetName()))


@click.command()
@click.option("--left", "-l", type=click.Path(exists=True), required=True)
@click.option("--right", "-r", type=click.Path(exists=True), required=True)
def main(left, right):
    """
    Use this script to compare the root files.
    Usage:
    python diff-resuts.py --left file1.root --right file2.root
    """
    ROOT.gROOT.cd()
    ROOT.gStyle.SetOptStat(False)

    hists1 = extract_data_lists(left)
    hists2 = extract_data_lists(right)

    not_reliable = []
    compare_lists_of_histograms(
        hists1, hists2, not_reliable, compare_bin_by_bin)
