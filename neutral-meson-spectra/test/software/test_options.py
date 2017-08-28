
import json
import unittest
import os

from spectrum.options import Options



class TestOptions(unittest.TestCase):


    def setUp(self):
        self.conffile = 'config/test_options.json'
        self.particle = 'pi0'
        data = {
                    "comment": "This file is needed for testing purpose only, feel free to delete it.",
                    "pi0": 
                    { 
                        "par_1": 1,
                        "par_2": [2, 7 ,3 ,4 ,5],
                        "par_3": ["3"],
                        "par_4": ["4"],
                        "par_5": 5,
                        "par_6": 6
                    }, 
                    "eta": 
                    { 
                        "par_1": 1,
                        "par_2": [2, 7 ,3 ,4 ,5],
                        "par_3": ["3"],
                        "par_4": ["4"],
                        "par_5": 5,
                        "par_6": 6
                    }
               }

        self.props = data[self.particle] 

        with open(self.conffile, 'w') as outfile:
            json.dump(data, outfile)

        # self.props.update({'par_6': 100})
        # self.props.update({'par_7': 100})

        # Enable debug output in the assertions
        self.longMessage = True


    def check(self, target, name):
        # Test keys
        for opt in self.props:
            msg = 'Key {} is missing in %s configuration' % name
            res = opt in dir(target)
            self.assertTrue(res, msg = msg.format(opt))


        for opt, val in self.props.iteritems():
            msg = 'The value of key {} differs in %s configuration' % name 
            res = target.__dict__[opt]
            self.assertEquals(res, val, msg = msg.format(opt, res))

    def test_spectrum(self):
        options = Options(spectrumconf = self.conffile)
        self.check(options.spectrum, 'spectrum')

    def test_pt(self):
        options = Options(ptconf = self.conffile)
        self.check(options.pt, 'pt')

    def test_invmass(self):
        options = Options(invmassconf = self.conffile)
        self.check(options.invmass, 'invmass')


    def tearDown(self):
        try:
            os.remove(self.conffile)
        except OSError:
            pass