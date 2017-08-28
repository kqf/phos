#!/usr/bin/python

import ROOT
import copy
from sutils import rebin_as

# TODO: Replace inheritance with factory moethods, and decorate cloning and copying?
# TODO: Make sure that all histograms have these properties
# TODO: Use decorators when it will be clear what fields are needed.

class Property(object):
    _properties = {'label': '', 'logy': 0, 'logx': 0, 'priority': 999, 'marker': 0}
    def __init__(self, label = '', logy = 0, logx = 0, priority = 999, marker = 0):
        super(Property, self).__init__()
        self.__dict__.update(self._properties)

        self.marker = marker
        self.label = label
        self.logy = logy
        self.logx = logx
        self.priority = priority
        # self.fitfunc = fitfunc

    def set_properties(self, source, force = False):
        assert self.has_properties(source), "There is no properties in source histogram"
        Property.copy_properties(self, source, force)

    def same_as(self, b):
        assert self.has_properties(b), "There is no properties in b histogram"
        return all(self.__dict__[prop] == b.__dict__[prop] for prop in self._properties) 

    @classmethod
    def update_properties(klass, hist, force = False):
        self = klass()
        klass.copy_properties(hist, self, force)

    @classmethod
    def copy_properties(klass, dest, source, force = False):
        assert klass.has_properties(source), "There is no properties in source histogram"

        keys = (key for key in klass._properties if key not in dir(dest) or force)
        for key in keys:
            # print dest.GetName(), 'added', key
            dest.__dict__[key] = copy.deepcopy(source.__dict__[key])

    @staticmethod
    def copy(dest, source):
        keys = (key for key in dir(source) if key not in dir(dest))
        for key in keys:
            dest.__dict__[key] = source.__dict__[key]

    @classmethod
    def has_properties(klass, hist):
        return all(prop in dir(hist) for prop in klass._properties) 

    @classmethod
    def ratio(klass, a, b, option = "B"):
        ratio = a.Clone('ratio' + a.GetName())
        klass.copy(ratio, a)

        if ratio.GetNbinsX() != b.GetNbinsX():
            ratio, b = rebin_as(ratio, b)

        ratio.Divide(a, b, 1, 1, option)
        label = a.label + ' / ' + b.label
        ratio.SetTitle('')
        ratio.GetYaxis().SetTitle(label)
        return ratio


# TODO: Add rebin_as function
# better histogram
class BH1F(ROOT.TH1F, Property):
    def __init__(self, *args, **kwargs):
        ROOT.TH1F.__init__(self, *args)
        Property.__init__(self, **kwargs)

    def Clone(self, name = "1"):
        hist = BH1F(self)
        hist.SetName(self.GetName() + name)
        hist.set_properties(self, force = True)
        return  hist

class BH1D(ROOT.TH1D, Property):
    def __init__(self, *args, **kwargs):
        ROOT.TH1D.__init__(self, *args)
        Property.__init__(self, **kwargs)

    def Clone(self, name = "1"):
        hist = BH1D(self)
        hist.SetName(self.GetName() + name)
        hist.set_properties(self, force = True)
        return  hist



class BH2F(ROOT.TH2F, Property):
    def __init__(self, *args, **kwargs):
        ROOT.TH2F.__init__(self, *args)
        Property.__init__(self, **kwargs)

    def Clone(self, name = "1"):
        hist = BH2F(self)
        hist.SetName(self.GetName() + name)
        hist.set_properties(self, force = True)
        return  hist

    def ProjectionX(self, name, a, b):
        hist = ROOT.TH2F.ProjectionX(self, name, a, b)
        hist = BH1D(hist)
        hist.set_properties(self, force = True)
        return hist
