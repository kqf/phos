import json
import sys


def dump_dict(dictionary):
    string = str(dictionary)
    with_newline = string.replace("{'", "{\n'")
    all_newline = with_newline.replace(", '", ",\n'")
    formatted = all_newline.replace("}", "\n}")
    return formatted.replace("'", '"')


def validate(test, output, path,
             outfile="config/test_values.json"):
    with open(outfile) as f:
        nominal = json.load(f)[sys.platform]

    for p in path.split('/'):
        nominal = nominal[p]

    for label, actual in output.iteritems():
        print 'Checking {}'.format(label)
        msg = '\n\n'
        msg += 'Nominal values:\n'
        msg += '"{}": {}\n'.format(label, nominal[label])
        msg += 'Actual values:\n'
        msg += '"{}": {}\n'.format(label, dump_dict(actual))
        for aa, bb in zip(actual, nominal[label]):
            test.assertAlmostEqual(aa, bb, msg=msg)
