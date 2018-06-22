import unittest
import json


class Validator(unittest.TestCase):

    def validate(self, output, outfile, path):
        with open(outfile) as f:
            nominal = json.load(f)

        for p in path.split('/'):
            nominal = nominal[p]

        msg = '\n\nActual values:\n' + str(output)
        for label, actual in output:
            print 'Checking {}'.format(label)
            for aa, bb in zip(actual, nominal[label]):
                self.assertAlmostEqual(aa, bb, msg=msg)
