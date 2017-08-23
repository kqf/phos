#!/usr/bin/python

import ROOT

# TODO: Make sure that all histograms have these properties

# TODO: Use decorators when it will be clear what fields are needed.

class Property(object):
    properties = {'label': '', 'logy': 1, 'logx': 0, 'priority': 999, 'marker': 0}
    def __init__(self, label = '', logy = 0, logx = 0, priority = 999, marker = 0):
        super(Property, self).__init__()
        self.__dict__.update(self.properties)

        self.marker = marker
        self.label = label
        self.logy = logy
        self.logx = logx
        self.priority = priority
        # self.fitfunc = fitfunc

    def set_properties(self, source, force = False):
        assert self.has_properties(source), "There is no properties in source histogram"
        Property.copy_properties(self, source, force)

    @classmethod
    def update_properties(klass, hist, force = False):
        self = klass()
        klass.copy_properties(hist, self, force)

    @staticmethod
    def copy_properties(dest, source, force = False):
        assert Property.has_properties(source), "There is no properties in source histogram"

        keys = (key for key in Property.properties if key not in dir(dest) or force)
        for key in keys:
            # print dest.GetName(), 'added', key
            dest.__dict__[key] = source.__dict__[key]

    @staticmethod
    def has_properties(hist):
        return all(prop in dir(hist) for prop in Property.properties) 

    def same_as(self, b):
        assert Property.has_properties(b), "There is no properties in b histogram"
        return all(self.__dict__[prop] == b.__dict__[prop] for prop in Property.properties) 


# TODO: Add rebin_as function
# better histogram
class BH1F(ROOT.TH1F, Property):
    def __init__(self, *args, **kwargs):
        ROOT.TH1F.__init__(self, *args)
        Property.__init__(self, **kwargs)

    def Clone(self, name = "1"):
        hist = BH1F(self)
        hist.SetName(self.GetName() + name)
        hist.set_properties(self)
        return  hist

class BH1D(ROOT.TH1D, Property):
    def __init__(self, *args, **kwargs):
        ROOT.TH1D.__init__(self, *args)
        Property.__init__(self, **kwargs)

    def Clone(self, name = "1"):
        hist = BH1D(self)
        hist.SetName(self.GetName() + name)
        hist.set_properties(self)
        return  hist



class BH2F(ROOT.TH2F, Property):
    def __init__(self, *args, **kwargs):
        ROOT.TH2F.__init__(self, *args)
        Property.__init__(self, **kwargs)

    def Clone(self, name = "1"):
        hist = BH2F(self)
        hist.SetName(self.GetName() + name)
        hist.set_properties(self)
        return  hist

    def ProjectionX(self, name, a, b):
        hist = ROOT.TH2F.ProjectionX(self, name, a, b)
        hist = BH1D(hist)
        hist.set_properties(self)
        return hist
