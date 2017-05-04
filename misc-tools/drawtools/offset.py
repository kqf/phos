#!/usr/bin/python

from drawtools.style import SingleStyler

import ROOT

ROOT.TH1.AddDirectory(False)

class Offset(SingleStyler):
    def __init__(self, data):
        super(Offset, self).__init__(data)


    def read_histogram(self, rpath, properties):
        obj = super(Offset, self).read_histogram(rpath, properties)

        if 'xoffset' in properties:
            obj.SetTitleOffset(properties['xoffset'], "X")


        if 'yoffset' in properties:
            obj.SetTitleOffset(properties['yoffset'], "Y")
