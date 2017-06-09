#!/usr/bin/python

import ROOT

# TODO: Make sure that all histograms have these properties

class Property(object):
    properties = {'label': '', 'logy': '', 'logx': '', 'priority': 999, 'fitfunc': None}
    def __init__(self, label = '', logy = '', logx = '', priority = 999, fitfunc = None):
        super(Property, self).__init__()
        self.__dict__.update(self.properties)

        self.label = label
        self.logy = logy
        self.logx = logx
        self.priority = priority
        self.fitfunc = fitfunc

    def set_properties(self, hist2):
        Property.copy_properties(self, hist2)

    @staticmethod
    def copy_properties(hist1, hist2):
        if 'label'    in dir(hist2): hist1.label = hist2.label
        if 'logy'     in dir(hist2): hist1.logy = hist2.logy
        if 'priority' in dir(hist2): hist1.priority = hist2.priority
        if 'fitfunc'  in dir(hist2): hist1.fitfunc = hist2.fitfunc
        return hist1


# better histogram
class BH1(ROOT.TH1F, Property):
    def __init__(self, *args, **kwargs):
        ROOT.TH1F.__init__(self, *args)
        Property.__init__(self, **kwargs)

    def Clone(self, name = "1"):
        hist = BH1(self)
        hist.SetName(self.GetName() + name)
        Property.copy_properties(hist, self)
        return  hist

class BH1D(ROOT.TH1D, Property):
    def __init__(self, *args, **kwargs):
        ROOT.TH1D.__init__(self, *args)
        Property.__init__(self, **kwargs)

    def Clone(self, name = "1"):
        hist = BH1D(self)
        hist.SetName(self.GetName() + name)
        Property.copy_properties(hist, self)
        return  hist



class BH2(ROOT.TH2F, Property):
    def __init__(self, *args, **kwargs):
        ROOT.TH2F.__init__(self, *args)
        Property.__init__(self, **kwargs)

    def Clone(self, name = "1"):
        hist = BH2(self)
        hist.SetName(self.GetName() + name)
        Property.copy_properties(hist, self)
        return  hist

    def ProjectionX(self, name, a, b):
        hist = ROOT.TH2F.ProjectionX(self, name, a, b)
        return BH1D(hist)


