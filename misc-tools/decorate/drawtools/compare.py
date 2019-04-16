import ROOT
import click


class Cc:
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"


def compare_visually(hist1, hist2):
    print hist1, hist2
    hist1.SetLineColor(37)
    hist2.SetLineColor(48)

    hist1.Draw()
    hist2.Draw("same")
    draw_and_save(hist1.GetName(), True, True)


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


def compare_chi(hist1, hist2):
    percentile = hist1.Chi2Test(hist2)
    if isclose(1., percentile):
        return  # everything is fine
    print "Rate of change of {} is {}".format(hist1.GetName(), percentile)


def isclose(a, b, rel_tol=1e-09):
    return abs(a - b) <= rel_tol


class Comparator(object):
    def __init__(self, ignore):
        super(Comparator, self).__init__()
        self.ignore = ignore

    def extract_data_list(self,
                          filename="AnalysisResults.root",
                          selection="PhysTender"):
        print "Processing  file:".format(filename)
        mfile = ROOT.TFile(filename)
        mlist = mfile.Get(selection)

        def hist_cut(h):
            res = h.GetEntries() > 0 and h.Integral() > 0
            if not res:
                print "Warning: Empty histogram found: {}".format(h.GetName())
            return res

        # mlist = [key.ReadObj().Clone() for key in mfile.GetListOfKeys()]
        # Don"t take empty histograms
        hists = [h for h in mlist if hist_cut(h)]
        return hists

    def find_similar_in(self, lst, ref):
        candidates = [h for h in lst if h.GetName() == ref.GetName()]
        if not candidates:
            msg = "There is no such histogram {} in second file or it's empty"
            print msg.format(ref.GetName())
            return None

        if len(candidates) > 1:
            print "You have multiple histograms with the same name!"
            print "(Assuming the first one)"

        return candidates[0]

    def compare_lists_of_histograms(self, l1, l2, compare=compare_chi):
        if len(l1) != len(l2):
            print "Warning files have different size".format(Cc.FAIL, )

        for h in l1:
            candidate = self.find_similar_in(l2, h)

            if (not candidate) or candidate.GetName() in self.ignore:
                continue
            compare(h, candidate)

        print "That's it!! The comparison is over."

    def compare_files(self, file1, file2, selection, comparator):
        hists1 = self.extract_data_list(file1, selection)
        hists2 = self.extract_data_list(file2, selection)
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


if __name__ == "__main__":
    main()
