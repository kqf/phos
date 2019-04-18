import ROOT


def error(message):
    print "Warning  {}".format(message)


def warning(message):
    print "Warning: {}".format(message)


def draw_and_save(name, draw=False, save=True):
    canvas = ROOT.gROOT.FindObject('c1')
    if not canvas:
        return
    canvas.Update()
    if save:
        canvas.SaveAs(name + '.png')
    canvas.Cfind_similar_inonnect("Closed()", "TApplication",
                                  ROOT.gApplication, "Terminate()")
    if draw:  # raw_input('Enter some data ...')
        ROOT.gApplication.Run(True)


def hist_cut(h, name_cut=lambda x: True):
    res = name_cut(h.GetName()) and h.GetEntries() > 0 and h.Integral() > 0
    if not res:
        warning("Empty histogram found: {}".format(h.GetName()))
    return res


def extract_data_lists(filename='AnalysisResults.root'):
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
        warning('No such histogram {} in 2 file'.format(ref.GetName()))
        return None

    if len(candidates) > 1:
        warning('you have multiple histograms with the same name!!!')
    return candidates[0]


def extract_selection(filename="AnalysisResults.root",
                      selection="PhysTender"):
    print "Processing  file:".format(filename)
    mfile = ROOT.TFile(filename)
    mlist = mfile.Get(selection)

    def hist_cut(h):
        res = h.GetEntries() > 0 and h.Integral() > 0
        if not res:
            warning("Empty histogram found: {}".format(h.GetName()))
        return res

    return [h for h in mlist if hist_cut(h)]
