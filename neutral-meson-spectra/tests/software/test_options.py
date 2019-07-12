from __future__ import print_function
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
    os.remove(conffile)


@pytest.mark.parametrize("name, target", [
    ("calibration", lambda x: Options(calibration=x).calibration),
    ("output", lambda x: Options(output=x).output),
    ("invmass", lambda x: Options(invmassconf=x).invmass),
])
def test_check_properties(name, target, props, conffile):
    # Test keys
    for opt in props:
        msg = "Key {{}} is missing in {} configuration".format(name)
        res = opt in dir(target(conffile))
        assert res, msg.format(opt)

    for opt, val in props.iteritems():
        msg = "The value of key {{}} differs in {} configuration".format(name)
        res = target(conffile).__dict__[opt]
        assert res == val, msg.format(opt, res)
