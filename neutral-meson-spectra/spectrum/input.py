#!/usr/bin/python

import ROOT
import os.path
from broot import BROOT as br


def read_histogram(filename, listname, histname, label = '', priority = 999, norm = False):
    hist = br.read.read(filename, listname, histname)
    br.set_nevents(hist, Input.events(filename, listname), norm)
    hist.priority = priority
    hist.label = label
    return hist

# TODO: Reimplement this for the case when we don't need mixed histogram
class Input(object):
    def __init__(self, filename, listname, histname = 'MassPt', mixprefix = 'Mix'):
        super(Input, self).__init__()
        self.filename = filename
        self.listname = listname
        self.histname = histname
        self.prefix = '', mixprefix
        self._events = self.events(filename, listname)

    @staticmethod
    def events(filename, listname):
        return br.read.read(filename, listname, 'EventCounter').GetBinContent(2)

    def read(self, histo = ''):
        # NB: Use histo to support per module histogram
        histo = histo if histo else self.histname
        raw_mix = ['h' + p + histo for p in self.prefix]
        raw_mix = br.read.read_multiple(self.filename, self.listname, raw_mix)

        for h in raw_mix:
            if not h: continue
            br.set_nevents(h, self._events)
        return raw_mix

    def read_per_module(self, threshold = 0.135):
        names = ['SM%dSM%d' % (i, j) for i in range(1, 5) for j in range(i, 5) if abs(i - j) < 2]
        data = map(lambda x: self.read(self.histname + x), names)

        good = lambda r: r or r.GetXaxis().GetBinCenter(r.FindFirstBinAbove(0)) > threshold 
        input_data = ((h, l) for h, l in zip(data, names) if good(h))
        return zip(*input_data)

class ExampleInput(Input):
    def __init__(self, filename, listname = 'Data', histname = 'MassPtA10vtx10', mixprefix = 'Mi'):
        super(ExampleInput, self).__init__(filename, listname, histname, mixprefix)


    @staticmethod
    def events(filename, listname):
        return br.read.read(filename, listname, 'hSelEvents').GetBinContent(4)

        
class TimecutInput(Input):
    def __init__(self, filename, listname, histname, mixprefix = 'Mix'):
        super(TimecutInput, self).__init__(filename, listname, histname, mixprefix)

    @staticmethod
    def events(filename, listname):
        return br.read.read(filename, 'PhysTender', 'EventCounter').GetBinContent(2)

