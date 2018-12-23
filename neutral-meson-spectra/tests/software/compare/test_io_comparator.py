import os

import ROOT
import spectrum.sutils as su
from spectrum.comparator import Comparator


def test_saves_output(data, stop, fname="test_io_deleteme.root"):
    ofile = ROOT.TFile(fname, "recreate")
    ofile.mkdir("test1/test2/")
    Comparator(stop=stop).compare(data)
    ofile.cd("test1/test2/")
    su.gcanvas().Write()
    ofile.Write()
    infile = ROOT.TFile(fname)
    infile.ls()
    os.remove(fname)
