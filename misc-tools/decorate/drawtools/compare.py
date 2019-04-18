import click
from drawtools.utils import draw_and_save, error, find_similar_in
from drawtools.utils import extract_selection, compare_chi


def compare_visually(hist1, hist2):
    print hist1, hist2
    hist1.SetLineColor(37)
    hist2.SetLineColor(48)

    hist1.Draw()
    hist2.Draw("same")
    draw_and_save(hist1.GetName(), True, True)


class Comparator(object):
    def __init__(self, ignore):
        super(Comparator, self).__init__()
        self.ignore = ignore

    def compare_lists_of_histograms(self, l1, l2, compare=compare_chi):
        # NB: Don't raise any assertions/exceptions, as it's expected to happen
        if len(l1) != len(l2):
            error("files have different size")

        for h in l1:
            candidate = find_similar_in(l2, h)

            if (not candidate) or candidate.GetName() in self.ignore:
                continue
            compare(h, candidate)
        print "That's it!! The comparison is over."

    def compare_files(self, file1, file2, selection, comparator):
        hists1 = extract_selection(file1, selection)
        hists2 = extract_selection(file2, selection)
        self.compare_lists_of_histograms(hists1, hists2, comparator)


@click.command()
@click.option('--first', '-f',
              type=click.Path(exists=True),
              help='Path to the first file',
              required=True)
@click.option('--second', '-s',
              type=click.Path(exists=True),
              help='Path to the second file')
@click.option('--selection',
              type=click.Path(exists=True),
              help='The requested selection')
def main(first, second, selection):
    """
    Use this script to compare the root files.
    Usage:
    python diff-resuts.py --first file1.root --second file2.root -selection SelectionName
    """  # noqa
    not_reliable = [""]
    diff = Comparator(not_reliable)
    diff.compare_files(first, second, selection, compare_chi)
