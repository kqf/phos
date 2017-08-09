#!/usr/bin/python


# TODO: Spilt this object across different configurables
# example 
#        options.spectrum.nsigmas = 5
#        options.spectrum.config = 'config/spectrum.json'
#        options.mass_range = (0.02, 0.06)


class AnalysisOption(object):
    def __init__(self, name, config):
        super(AnalysisOption, self).__init__()
        self.name = name
        self.config = config


class Options(object):
    """
        This is class should handle all possible variable! options 
        that i need to compare in my analysis.
    """
    def __init__(self, label = 'data', mode = 'q', relaxedcb = False, particle='pi0', average = {}, priority = 999):
        super(Options, self).__init__()
        self.particle = particle

        self.spectrum = AnalysisOption('spectrum', 'config/spectrum.json')
        self.spectrum.fit_mass_width = True
        self.spectrum.nsigmas = 2

        self.pt = AnalysisOption('ptanalysis', 'config/pt-analysis.json')
        self.pt.priority = 999
        self.pt.label = label
        self.pt.mode = 'q'

        self.invmass  = AnalysisOption('invmass', 'config/invariant-mass.json')
        self.invmass.relaxedcb = relaxedcb
        self.invmass.average  = average
        self.invmass.ispi0 = 'pi0' in self.particle

    @staticmethod
    def fixed_peak(*args):
        options = Options(*args)
        options.spectrum.fit_mass_width = False
        options.mode = 'd'
        return options


