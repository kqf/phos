#!/usr/bin/python

import ROOT
import os.path


def read_root_file(name, directory = 'input-data/'):
    if os.path.isfile(name):
        return ROOT.TFile(name) 

    if not directory in name:
        return read_root_file(directory + name, directory)

    if not '.root' in name:
        return read_root_file(name + '.root', directory)

    raise IOError('No such file: {0}'.format(name))



def read_histogram(filename, listname, histname, label = None, priority = 999, norm = False):
    infile = read_root_file(filename)
    lst    = infile.Get(listname)
    hist   = lst.FindObject(histname)

    if not hist: 
        return None

    Input.events(lst, hist, norm)


    hist.label    = label if label else '' 
    hist.priority = priority
    return hist


class Input(object):
    def __init__(self, filename, listname, histname = 'MassPtN3', mixprefix = 'Mix'):
        super(Input, self).__init__()
        self.filename = filename
        self.listname = listname
        self.histname = histname
        self.mixprefix = mixprefix
        self.infile = read_root_file(self.filename) 

    @staticmethod
    def events(lst, hist, norm = False):
        hist.nevents = lst.FindObject('EventCounter').GetBinContent(2)
        if norm:
            hist.Scale(1. / hist.nevents)

    def hist(self, lst, name):
        hist = lst.FindObject('h' + name)
        if not hist:
            return None

        # Don't normalize input histograms
        self.events(lst, hist) 
        return hist

    def read(self, hname = ''):
        if not hname: hname = self.histname

        lst = self.infile.Get(self.listname)

        raw, mix =  self.hist(lst, hname), self.hist(lst, self.mixprefix + hname)
        return raw, mix

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


    def hist(self, lst, name):
        hist = lst.FindObject('h' + name)
        if not hist:
            return None

        # Don't normalize input histograms
        # Make shure that we have event counter from PhysTender
        #
        self.events(self.infile.PhysTender, hist) 
        return hist    
