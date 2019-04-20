import ROOT


def remove2dir(filename, selname):
    infile = ROOT.TFile(filename, "update")
    selection = infile.Get(selname)
    selection.Write(selection.GetName(), 1)
    infile.Write()
    infile.Close()
