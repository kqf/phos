import json
import sys
import six
import numpy as np


def dump_dict(dictionary):
    string = str(dictionary)
    with_newline = string.replace("{'", "{\n'")
    all_newline = with_newline.replace(", '", ",\n'")
    formatted = all_newline.replace("}", "\n}")
    return formatted.replace("'", '"')


def validate(output, path,
             outfile="config/test_values.json"):
    with open(outfile) as f:
        nominal = json.load(f)[sys.platform]

    for p in path.split('/'):
        nominal = nominal[p]

    # TODO: Should one iterate over nominal or actual values?
    msg = '\n\n'
    msg += 'Actual values:\n'
    for label, actual in six.iteritems(nominal):
        msg += '"{}": {},\n'.format(label, dump_dict(actual))

    for label, actual in six.iteritems(nominal):
        print('Checking {}'.format(label))
        np.testing.assert_almost_equal(actual, nominal[label], err_msg=msg)
