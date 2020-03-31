import json
import sys
import six
import numpy as np


def dump_dict(dictionary):
    string = (
        str(dictionary)
        .replace("{'", "{\n'")
        .replace(", '", ",\n'")
        .replace("}", "\n}")
        .replace("'", '"')
    )
    return string


def validate(output, path,
             outfile="config/tests/values.json"):
    with open(outfile) as f:
        nominal = json.load(f)[sys.platform]

    for p in path.split('/'):
        nominal = nominal[p]

    msg = '\n\n'
    msg += 'Actual values:\n'
    for label, actual in six.iteritems(nominal):
        msg += '"{}": {},\n'.format(label, dump_dict(actual))

    for label, actual in six.iteritems(nominal):
        print('Checking {}'.format(label))
        np.testing.assert_almost_equal(actual, nominal[label], err_msg=msg)
