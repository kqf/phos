#!/usr/bin/python

import ROOT
import copy
from sutils import rebin_as

# TODO: Finalize BROOT class
# TODO: Add rebin_as function

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



class BROOT(object):
    def __init__(self):
        super(BROOT, self).__init__()

    @staticmethod
    def BH(THnT, *args, **kwargs):
        hist = THnT(*args)
        Property.copy_properties(hist, Property(**kwargs))
        return hist

    @staticmethod
    def clone(hist, name = '_copied', replace = False):
        name = name if replace else hist.GetName() + name 
        cloned = hist.Clone(name)
        Property.copy_properties(cloned, hist)
        return cloned

    @staticmethod
    def copy(hist, name = '_copied', replace = False):
        return BROOT.clone(hist, name, replace)


    @staticmethod
    def projection(hist, name, a, b, axis = 'x'):
        pass
        # f = lambda x: x.ProjectionX if axis.lower() == 'x' else lambda x: x.ProjectionY
        # proj = f(hist)(name, a, b)
        # proj = BH1D(proj)
        # Property.set_properties(self, force = True)
        # returnproj 
