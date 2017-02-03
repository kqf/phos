#!/usr/bin/python

import ROOT
class Input(object):
    def __init__(self, filename, listname, histname = 'MassPtN3', mixprefix = 'Mix'):
        super(Input, self).__init__()
        self.filename = filename
        self.listname = listname
        self.histname = histname
        self.mixprefix = mixprefix
        self.infile = ROOT.TFile(filename)

    def events(self, lst):
        return lst.FindObject('EventCounter').GetBinContent(2)

    def read(self, hname = ''):
        if not hname: hname = self.histname

        lst = self.infile.Get(self.listname)
        hist = lambda n: lst.FindObject('h' + n)

        n, raw, mix = self.events(lst), hist(hname), hist(self.mixprefix + hname)
        raw.nevents = n
        mix.nevents = n
        return n, raw, mix

    def read_per_module(self, threshold = 0.135):
        names = ['SM%dSM%d' % (i, j) for i in range(1, 5) for j in range(i, 5) if abs(i - j) < 2]
        data = map(lambda x: self.read(self.histname + x), names)

        good = lambda r: r or r.GetXaxis().GetBinCenter(r.FindFirstBinAbove(0)) > threshold 
        input_data = ((h, l) for h, l in zip(data, names) if good(h))
        return zip(*input_data)


class ExampleInput(Input):
    def __init__(self, filename, listname = 'Data', histname = 'MassPtA10vtx10', mixprefix = 'Mi'):
        super(ExampleInput, self).__init__(filename, listname, histname, mixprefix)

    def events(self, lst):
        return lst.FindObject('hSelEvents').GetBinContent(4)
        
class TimecutInput(Input):
    def __init__(self, filename, listname, histname, mixprefix = 'Mix'):
        super(TimecutInput, self).__init__(filename, listname, histname, mixprefix)

    def events(self, lst):
        lst = self.infile.PhysTender
        return lst.FindObject('EventCounter').GetBinContent(2)
