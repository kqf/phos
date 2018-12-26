import pytest
import json
import os

from spectrum.options import Options


@pytest.fixture(scope="module")
def conffile():
    return "config/test_options.json"


@pytest.fixture(scope="module")
def props(conffile):
    particle = "#pi^{0}"
    data = {
        "comment":
            "This file is needed for testing purpose only, " +
            "feel free to delete it.",
        "#pi^{0}":
        {
            "par_1": 1,
            "par_2": [2, 7, 3, 4, 5],
            "par_3": ["3"],
            "par_4": ["4"],
            "par_5": 5,
            "par_6": 6
        },
        "#eta":
        {
            "par_1": 1,
            "par_2": [2, 7, 3, 4, 5],
            "par_3": ["3"],
            "par_4": ["4"],
            "par_5": 5,
            "par_6": 6
        }
    }

    props = data[particle]

    with open(conffile, "w") as outfile:
        json.dump(data, outfile)
    yield props
    try:
        os.remove(conffile)
    except OSError:
        pass


def check(target, props, name):
    # Test keys
    for opt in props:
        msg = "Key {} is missing in %s configuration" % name
        res = opt in dir(target)
        assert res, msg.format(opt)

    for opt, val in props.iteritems():
        msg = "The value of key {} differs in %s configuration" % name
        res = target.__dict__[opt]
        assert res == val, msg.format(opt, res)


def test_spectrum(conffile, props):
    options = Options(spectrumconf=conffile)
    check(options.spectrum, props, "spectrum")


def test_pt(conffile, props):
    options = Options(outconf=conffile)
    check(options.output, props, "output")


def test_invmass(conffile, props):
    options = Options(invmassconf=conffile)
    check(options.invmass, props, "invmass")


def test_rebins():
    option = Options()
    # print "ptedges before", option.pt.ptedges
    edg_before = len(option.pt.ptedges)
    Options.coarse_binning(option)
    # print "ptedges edges", option.pt.ptedges

    edg_after = len(option.pt.ptedges)
    reb_after = len(option.pt.rebins)

    # Check if the data is consistent
    assert edg_after - 1 == reb_after

    # The binning is indeed coarse
    assert edg_after < edg_before
