#!/usr/bin/python


# TODO: Spilt this object across different configurables
# example 
#        options.spectrum.nsigmas = 5
#        options.spectrum.config = 'config/spectrum.json'
#        options.mass_range = (0.02, 0.06)

import json


class AnalysisOption(object):
    ignore_attributes = 'eta', 'pi0', 'comment'

    def __init__(self, name, config, particle):
        super(AnalysisOption, self).__init__()
        self.name = name
        with open(config) as f:
            conf = json.load(f)
        self._setup_configurations(conf, particle)


    def _setup_configurations(self, conf, particle):
        self._update_variables(conf)

        if not particle in conf:
            return

        conf = conf[particle]
        self._update_variables(conf)


    def _update_variables(self, vardict):
        items = (k for k in vardict if not k in self.ignore_attributes)
        for n in items:
            # print n, vardict[n]
            setattr(self, n, vardict[n])



class Options(object):
    """
        This is class should handle all possible variable! options 
        that i need to compare in my analysis.
    """
    def __init__(self, label = 'data', mode = 'q', relaxedcb = False, particle='pi0', average = {}, priority = 999):
        super(Options, self).__init__()
        self.spectrum = AnalysisOption('spectrum', 'config/spectrum.json', particle)
        self.pt = AnalysisOption('ptanalysis', 'config/pt-analysis.json', particle)
        self.pt.priority = priority
        self.pt.label = label
        self.pt.mode = mode

        self.invmass = AnalysisOption('invmass', 'config/invariant-mass.json', particle)
        self.invmass.relaxedcb = relaxedcb
        self.invmass.average  = average
        self.invmass.ispi0 = 'pi0' in particle

    @staticmethod
    def fixed_peak(*args):
        options = Options(*args)
        options.spectrum.fit_mass_width = False
        options.mode = 'd'
        return options


