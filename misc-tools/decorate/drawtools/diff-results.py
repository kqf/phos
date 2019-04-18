import ROOT
import click
from drawtools.utils import extract_data_lists, draw_and_save, find_similar_in
from drawtools.utils import error, compare_chi


def compare_bin_by_bin(hist1, hist2):
    i1, i2 = hist1.Integral(), hist2.Integral()
    if int(i1 - i2) != 0:
        return error(
            'The histograms {} are different. Int1 - Int2 = {}'.format(
                hist1.GetName(), str(i1 - i2)))

    def f(x):
        return [x.GetBinContent(i + 1) for i in range(x.GetNbinsX())]
    if not f(hist1) == [i for i in f(hist2)]:
        error('Some bins are different in ' + hist1.GetName())
    print 'Histograms are'.format(hist1.GetName())


def compare_visually(hist1, hist2):
    hist1.SetLineColor(37)
    hist2.SetLineColor(48)

    a, b = hist1.GetXaxis().GetNbins(), hist1.GetXaxis().GetNbins()
    print a, b
    x, y = hist1.GetYaxis().GetNbins(), hist1.GetYaxis().GetNbins()
    print x, y

    print hist1.GetXaxis().GetBinCenter(1), hist1.GetXaxis().GetBinCenter(1)
    print hist1.GetXaxis().GetBinCenter(a), hist1.GetXaxis().GetBinCenter(b)
    print hist1.GetYaxis().GetBinCenter(1), hist1.GetYaxis().GetBinCenter(1)
    print hist1.GetYaxis().GetBinCenter(x), hist1.GetYaxis().GetBinCenter(y)

    hist = hist1.Clone('diff')
    hist.SetTitle(hist1.label + ' - ' + hist2.label +
                  ' , ' + hist1.GetName().split('_')[-1])
    hist.Add(hist2, -1)
    hist.Draw('colz')

    draw_and_save(hist1.GetName(), True, True)


def fsum(lst):
    return fsum(i.GetEntries() for i in lst)


def compare_lists_of_histograms(l1, l2, ignore=[], compare=compare_chi):
    if len(l1) != len(l2):
        print 'Warning files have different shape'
    if fsum(l1) != fsum(l2):
        print 'Total entries in the the lists: {} {}'.format(
            fsum(l1), fsum(l2))

    for h in l1:
        candidate = find_similar_in(l2, h)
        if not candidate or candidate.GetName() in ignore:
            continue
        compare(h, candidate)

    print "That's it!! Your computation is done"


def compare_histograms(left, right):
    ROOT.gROOT.cd()
    ROOT.gStyle.SetOptStat(False)

    hists1 = extract_data_lists(left)
    hists2 = extract_data_lists(right)

    not_reliable = []
    compare_lists_of_histograms(
        hists1, hists2, not_reliable, compare_bin_by_bin)


@click.command()
@click.option('--left', '-l',
              type=click.Path(exists=True),
              help='Path to the first file',
              required=True)
@click.option('--right', '-r',
              type=click.Path(exists=True),
              help='Path to the second file')
def main(left, right):
    """
    Use this script to compare the root files.
    Usage:
    python diff-resuts.py --left file1.root --right file2.root
    """
    compare_histograms(left, right)


if __name__ == '__main__':
    main()
