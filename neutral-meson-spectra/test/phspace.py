#!/usr/bin/python


import ROOT


class InclusiveGenerator(object):
    def __init__(self, fname, selname = 'PhysTender', hnames = ['hMassPtN3', 'hMixMassPtN3', 'EventCounter']):
        super(InclusiveGenerator, self).__init__()
        self.selname = selname
        self.data = self.read(fname, hnames)


    def read(self, fname, hnames):
        lst = ROOT.TFile(fname).Get(self.selname)
        hist = lambda n: lst.FindObject(n)
        return map(hist, hnames)


    def save_fake(self, fname):
        ofile = ROOT.TFile(fname, 'recreate')
        olist = ROOT.TList()
        for i in self.data: olist.Add(i)
        olist.Write(self.selname, 1)
        ofile.Close()


    def real_distributions(self):
        pass


