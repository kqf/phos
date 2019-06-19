import pytest
import os

import ROOT
import spectrum.sutils as su
from spectrum.comparator import Comparator


@pytest.fixture
def fname():
    name = "test_io_deleteme.root"
    yield name
    os.remove(name)


def test_saves_output(data, stop, fname):
    with su.rfile(fname) as ofile:
        ofile.mkdir("test1/test2/")
        Comparator(stop=stop).compare(data)

        ofile.cd("test1/test2/")
        su.gcanvas().Write()

    with su.rfile(fname, "read") as infile:
        infile = ROOT.TFile(fname)
        infile.ls()

    assert os.path.isfile(fname)
