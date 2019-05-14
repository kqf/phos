import json
import sys
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

    msg = '\n\n'
    # for label, actual in output.iteritems():
    #     msg += 'Nominal values:\n'
    #     msg += '"{}": {}\n'.format(label, nominal[label])
    msg += 'Actual values:\n'
    for label, actual in output.iteritems():
        msg += '"{}": {},\n'.format(label, dump_dict(actual))

    for label, actual in output.iteritems():
        print 'Checking {}'.format(label)
        np.testing.assert_almost_equal(actual, nominal[label], err_msg=msg)
