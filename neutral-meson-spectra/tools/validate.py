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

    msg = '\n\nActual values:\n' + dump_dict(output)
    for label, actual in output.iteritems():
        print 'Checking {}'.format(label)
        for aa, bb in zip(actual, nominal[label]):
            test.assertAlmostEqual(aa, bb, msg=msg)
