#!/usr/bin/python

import ROOT
import os.path
from broot import BROOT as br


def read_histogram(filename, listname, histname, label = '', priority = 999, norm = False):
    hist = br.io.read(filename, listname, histname)
    br.set_nevents(hist, Input.events(filename, listname), norm)
    hist.priority = priority
    hist.label = label
    return hist

class Input(object):
    def __init__(self, filename, listname, histname = 'MassPt', label='', mixprefix = 'Mix'):
        super(Input, self).__init__()
        self.filename = filename
        self.listname = listname
        self.histname = histname
        self.prefix = '', mixprefix
        self._events = self.events(filename, listname)
        self.label = label

    @staticmethod
    def events(filename, listname):
        return br.io.read(filename, listname, 'EventCounter').GetBinContent(2)

    def read(self, histo = ''):
        # NB: Use histo to support per module histogram
        histo = histo if histo else self.histname
        raw_mix = ['h' + p + histo for p in self.prefix]
        raw_mix = br.io.read_multiple(self.filename, self.listname, raw_mix)

        for h in raw_mix:
            if not h: continue
            br.set_nevents(h, self._events)
        return raw_mix

    def transform(self, data = None):
        return self.read()


    @classmethod
    def read_per_module(klass, filename, listname,
        histname = 'MassPt', label='', mixprefix='Mix'):
        names = ['SM%dSM%d' % (i, j) for i in range(1, 5) for j in range(i, 5) if abs(i - j) < 2]

        output = [klass(
            filename,
            listname,
            histname + x,
            label=x,
            mixprefix=mixprefix
        ) for x in names]

        return output

class NoMixingInput(Input):
    def __init__(self, filename, listname, histname = 'MassPt', label='', mixprefix = 'Mix'):
        super(NoMixingInput, self).__init__(filename, listname, histname, label, mixprefix)

    def read(self, histo = ''):
        histo = histo if histo else self.histname
        raw = br.io.read(self.filename, self.listname, 'h' + histo)
        br.set_nevents(raw, self._events)
        return raw, None

class ExampleInput(Input):
    def __init__(self, filename, listname = 'Data', histname = 'MassPtA10vtx10', mixprefix = 'Mi'):
        super(ExampleInput, self).__init__(filename, listname, histname, mixprefix)


    @staticmethod
    def events(filename, listname):
        return br.io.read(filename, listname, 'hSelEvents').GetBinContent(4)

        
class TimecutInput(Input):
    def __init__(self, filename, listname, histname, mixprefix = 'Mix'):
        super(TimecutInput, self).__init__(filename, listname, histname, mixprefix)

    @staticmethod
    def events(filename, listname):
        return br.io.read(filename, 'PhysTender', 'EventCounter').GetBinContent(2)

