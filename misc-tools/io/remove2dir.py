import sys
import ROOT

# PHOSEpRatio / PHOSEpRatioCoutput1


def main():
    filename, dirname, selname = sys.argv[1:]
    print "From file", dirname, "and folder", dirname, "selct", "selname"

    infile = ROOT.TFile(filename, "update")
    selection = infile.Get("{}/{}".format(dirname, selname))
    selection.Write(selname, 1)
    infile.Write()
    infile.Close()


if __name__ == '__main__':
    main()
