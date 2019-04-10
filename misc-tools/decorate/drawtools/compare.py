import ROOT
import sys
ROOT.gROOT.cd()


class Cc:
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


def compare_visually(hist1, hist2):
    print hist1, hist2
    hist1.SetLineColor(37)
    hist2.SetLineColor(48)

    hist1.Draw()
    hist2.Draw('same')
    draw_and_save(hist1.GetName(), True, True)


def draw_and_save(name, draw=False, save=True):
    canvas = ROOT.gROOT.FindObject('c1')
    if not canvas:
        return
    canvas.Update()
    if save:
        canvas.SaveAs(name + '.png')
    canvas.Connect("Closed()", "TApplication",
                   ROOT.gApplication, "Terminate()")
    if draw:  # raw_input('Enter some data ...')
        ROOT.gApplication.Run(True)


def compare_chi(hist1, hist2):
    percentile = hist1.Chi2Test(hist2)
    if isclose(1., percentile):
        return  # everything is fine
    msg = '{0}Rate of change of {1}{2}{0} is {1}{3}{0} {4}'
    print msg.format(Cc.WARNING, Cc.OKGREEN,
                     hist1.GetName(), percentile, Cc.ENDC)


def isclose(a, b, rel_tol=1e-09):
    return abs(a - b) <= rel_tol


class Comparator(object):
    def __init__(self, ignore):
        super(Comparator, self).__init__()
        self.ignore = ignore

    def get_list(self, filename='AnalysisResults.root', selection='PhysTender'):
        print 'Processing {0} file:'.format(filename)
        mfile = ROOT.TFile(filename)
        mlist = mfile.Get(selection)

        def hist_cut(h):
            res = h.GetEntries() > 0 and h.Integral() > 0  # and h.GetBinContent(1) > 10
            if not res:
                print '{0}Warning: Empty histogram found: {1} {2}'.format(Cc.WARNING, h.GetName(), Cc.ENDC)
            return res

        # mlist = [key.ReadObj().Clone() for key in mfile.GetListOfKeys()]
        # Don't take empty histograms
        hists = [h for h in mlist if hist_cut(h)]
        return hists

    def find_similar_in(self, lst, ref):
        candidates = [h for h in lst if h.GetName() == ref.GetName()]
        if not candidates:
            print '{0}Warning: There is no such histogram {1}{2}{0} in second file or it\'s empty{3}'.format(Cc.WARNING, Cc.OKGREEN, ref.GetName(), Cc.ENDC)
            return None

        if len(candidates) > 1:
            print '{0}Warning: you have multiple histograms with the same name!!! Act!!{1}'.format(Cc.Warning, Cc.ENDC)

        return candidates[0]

    def compare_lists_of_histograms(self, l1, l2, compare=compare_chi):
        if len(l1) != len(l2):
            print '{0}Warning files have different size{1}'.format(Cc.FAIL, Cc.ENDC)

        for h in l1:
            candidate = self.find_similar_in(l2, h)

            if (not candidate) or candidate.GetName() in self.ignore:
                continue
            compare(h, candidate)

        print "That's it!! The comparison is over."

    def compare_files(self, file1, file2, selection, comparator):
        hists1 = self.get_list(file1, selection)
        hists2 = self.get_list(file2, selection)
        self.compare_lists_of_histograms(hists1, hists2, comparator)


def main():
    not_reliable = [""]

    if len(sys.argv) != 4:
        print 'Invalid number of arguments.\nExample: file1.root file2.root SelectionName'
        raise ValueError(
            'Invalid number of arguments.\nExample: file1.root file2.root SelectionName')

    diff = Comparator(not_reliable)
    file1, file2, selection = sys.argv[1:4]
    #
    # diff.compare_files(file1, file2, selection, compare_visually)

    # If you are using lxplus it's better to use Chi^2 test
    diff.compare_files(file1, file2, selection, compare_chi)


if __name__ == '__main__':
    main()
