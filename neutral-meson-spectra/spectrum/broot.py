#!/usr/bin/python

import ROOT

import os
import copy
from sutils import rebin_as

# TODO: Add rebin_as function
class BROOT(object):
    class prop(object):
        _properties = {'label': '', 'logy': 0, 'logx': 0, 'priority': 999, 'marker': 0}
        def __init__(self, label = '', logy = 0, logx = 0, priority = 999, marker = 0):
            super(BROOT.prop, self).__init__()
            self.__dict__.update(self._properties)
            # Add self.set_properties
            self.marker = marker
            self.label = label
            self.logy = logy
            self.logx = logx
            self.priority = priority
            # self.fitfunc = fitfunc

        def set_properties(self, source, force = False):
            assert self.has_properties(source), "There is no properties in source histogram"
            self.copy(self, source, force)

        @classmethod
        def same_as(klass, a, b):
            assert klass.has_properties(b), "There is no properties in b histogram"
            return all(a.__dict__[prop] == b.__dict__[prop] for prop in klass._properties) 

        @classmethod
        def init(klass, hist, force = True):
            self = klass()
            klass.copy(hist, self, force)

        @classmethod
        def copy(klass, dest, source, force = False):
            assert klass.has_properties(source), "There is no properties in source histogram"

            keys = (key for key in klass._properties if key not in dir(dest) or force)
            for key in keys:
                # print dest.GetName(), 'added', key
                dest.__dict__[key] = copy.deepcopy(source.__dict__[key])

        @staticmethod
        def copy_everything(dest, source):
            keys = (key for key in dir(source) if key not in dir(dest))
            for key in keys:
                dest.__dict__[key] = source.__dict__[key]

        @classmethod
        def has_properties(klass, hist):
            return all(prop in dir(hist) for prop in klass._properties) 

    class read(object):
        def __init__(self):
            super(BROOT.read, self).__init__()

        @staticmethod
        def _read_file(filename):
            if os.path.isfile(filename):
                return ROOT.TFile(filename) 
            raise IOError('No such file: {0}'.format(filename))

        @classmethod
        def _read_list(klass, filename, selection):
            infile = klass._read_file(filename)
            lst = infile.Get(selection)

            if not lst:
                infile.ls()
                raise IOError('No such selection {1} in file: \
                    {0}'.format(filename, selection))
            return lst

        @classmethod
        def read(klass, filename, selection, histname):
            lst = klass._read_list(filename, selection)
            hist = lst.FindObject(histname)

            if not hist:
                raise IOError('No such histogram {2} for selection {1} in file: ' + \
                    '{0}'.format(filename, selection, histname))

            BROOT.prop.init(hist)
            return hist

            
    def __init__(self):
        super(BROOT, self).__init__()

    @classmethod
    def BH(klass, THnT, *args, **kwargs):
        hist = THnT(*args)
        klass.setp(hist, klass.prop(**kwargs))
        return hist

    @classmethod
    def setp(klass, dest, source, force = False):
        if not source: source = klass.prop()
        klass.prop.copy(dest, source, force)

    @classmethod
    def clone(klass, hist, name = '_copied', replace = False):
        name = name if replace else hist.GetName() + name 
        cloned = hist.Clone(name)
        klass.setp(cloned, hist)
        return cloned

    # TODO: Add test for this
    @classmethod
    def copy(klass, hist, name = '_copied', replace = False):
        hist = BROOT.clone(hist, name, replace)
        hist.Reset()
        return hist

    @classmethod
    def projection(klass, hist, name, a, b, axis = 'x'):
        axis, name = axis.lower(), hist.GetName() + name
        proj = hist.ProjectionX(name, a, b) if axis == 'x' else hist.ProjectionY(name, a, b)
        klass.setp(proj, hist, force = True)
        return proj

    @classmethod
    def same(klass, hist1, hist2):
        if klass.prop.has_properties(hist1):
            return klass.prop.same_as(hist2, hist1)

        if klass.prop.has_properties(hist2):
            return klass.prop.same_as(hist1, hist2)

        raise AttributeError('Neither of hist1 and hist2 have BROOT properties')

    @classmethod
    def ratio(klass, a, b, option = "B"):
        ratio = a.Clone('ratio' + a.GetName())
        klass.prop.copy_everything(ratio, a)

        if ratio.GetNbinsX() != b.GetNbinsX():
            ratio, b = rebin_as(ratio, b)

        ratio.Divide(a, b, 1, 1, option)
        label = a.label + ' / ' + b.label
        ratio.SetTitle('')
        ratio.GetYaxis().SetTitle(label)
        return ratio
