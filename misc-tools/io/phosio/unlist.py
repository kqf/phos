import sys
import ROOT

# Usage
# python flatten.py ./path/to/file "Phys/MassPt"


def unlist(filename, dirname, histname):
    infile = ROOT.TFile(filename, "update")
    selection = infile.Get(dirname)
    selection.ls()

    ohist = selection.FindObject(histname)
    infile.Close()

    ofile = ROOT.TFile("flattened.root", "update")
    ohist.Write()
    ofile.Close()


def main():
    filename, path = sys.argv[1:]
    unlist(filename, *path.split("/"))


if __name__ == '__main__':
    main()
