import sys
import ROOT

# Usage
# python flatten.py ./path/to/file Phys MassPt


def main():
    filename, dirname, histname = sys.argv[1:]
    print "From file", dirname, "and folder", dirname, "select", histname

    infile = ROOT.TFile(filename, "update")
    selection = infile.Get(dirname)
    selection.ls()

    ohist = selection.FindObject(histname)
    infile.Close()

    ofile = ROOT.TFile("flattened.root", "update")
    ohist.Write()
    ofile.Close()


if __name__ == '__main__':
    main()
