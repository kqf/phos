import ROOT
import sys


def error(s):
    print s


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


def hist_cut(h, namecut=lambda x: True):
    res = namecut(h.GetName()) and h.GetEntries() > 0 and h.Integral() > 0
    if not res:
        print "Warning: Empty histogram found: {}".format(h.GetName())
    return res


def get_my_list(filename='AnalysisResults.root'):
    print 'Processing %s file:' % filename
    mfile = ROOT.TFile(filename)
    # Without this line your Clones are created inside FILENAME directory.
    # mfile -> local, so this object will when we reach the end of this
    # function.Therefore ROOT this direcotry and all its will be destroyed.
    ROOT.gROOT.cd()
    mlist = [key.ReadObj().Clone() for key in mfile.GetListOfKeys()]
    hists = [h for h in mlist if hist_cut(h)]  # Don't take empty histograms
    for h in hists:
        h.label = filename.split('_')[-1].replace('.root', '')
    return hists


def find_similar_in(lst, ref):
    candidates = [h for h in lst if h.GetName() == ref.GetName()]
    if not candidates:
        print 'Warning: There is no such histogram {} in 2 file'.format(
            ref.GetName()
        )
        return None

    if len(candidates) > 1:
        print 'Warning: you have multiple histograms with the same name!!!'
    return candidates[0]


def isclose(a, b, rel_tol=1e-09):
    return abs(a - b) <= rel_tol


def compare_chi(hist1, hist2):
    percentile = hist1.Chi2Test(hist2)
    if isclose(1., percentile):
        return  # everything is fine
    print 'Rate of change of {} is {}'.format(hist1.GetName(), percentile)


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


def compare_histograms():
    ROOT.gROOT.cd()
    ROOT.gStyle.SetOptStat(False)

    hists1 = get_my_list(sys.argv[1])
    hists2 = get_my_list(sys.argv[2])

    not_reliable = []
    compare_lists_of_histograms(
        hists1, hists2, not_reliable, compare_bin_by_bin)


def main():
    assert len(sys.argv) > 2, 'Usage: diff-results file1.root file2.root'
    compare_histograms()


if __name__ == '__main__':
    main()
