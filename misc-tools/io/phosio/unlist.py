import ROOT


def unlist(filename, dirname, histname):
    infile = ROOT.TFile(filename, "update")
    selection = infile.Get(dirname)
    selection.ls()

    ohist = selection.FindObject(histname)
    infile.Close()

    ofile = ROOT.TFile("flattened.root", "update")
    ohist.Write()
    ofile.Close()
