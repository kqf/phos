import sys
import ROOT

# Usage
# python remove2dir.py ./path/to/file "PHOSEpRatio/PHOSEpRatioCoutput1"


def remove2dir(filename, selname):
    infile = ROOT.TFile(filename, "update")
    selection = infile.Get(selname)
    selection.Write(selection.GetName(), 1)
    infile.Write()
    infile.Close()


def main():
    filename, selname = sys.argv[1:]
    print "From file", filename, "select", selname
    remove2dir(filename, selname)


if __name__ == '__main__':
    main()
