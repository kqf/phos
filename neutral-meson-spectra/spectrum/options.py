#!/usr/bin/python


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
    modes = {'quiet': False, 'q': False , 'silent': False, 's': False, 'dead': False, 'd': False}

    def __init__(self, label = 'data', mode = 'q', relaxedcb = False, particle='pi0', average = {}, priority = 999, fitf = 'cball'):
        super(Options, self).__init__()
        show_img = self.modes.get(mode, True)

        self.spectrum = AnalysisOption('spectrum', 'config/spectrum.json', particle)
        self.spectrum.show_img = show_img

        self.pt = AnalysisOption('ptanalysis', 'config/pt-analysis.json', particle)
        self.pt.priority = priority
        self.pt.label = label
        self.pt.show_img = show_img
        self.pt.dead_mode = 'd' in mode

        self.invmass = AnalysisOption('invmass', 'config/invariant-mass.json', particle)
        self.invmass.average = average

        pconf = 'config/{0}-parameters.json'.format('gaus' if 'gaus' in fitf.lower() else 'cball')
        self.param = AnalysisOption('param', pconf, particle)
        self.param.relaxed = relaxedcb
        # TODO: Deleteme?
        self.param.ispi0 = 'pi0' in particle

    @property
    def fitf(self):
        return self.param.fitf

    @fitf.setter
    def fitf(self, fitf):
        r, p = self.param.relaxed, self.param.ispi0 
        pconf = 'config/gaus-parameters.json' if 'gaus' in fitf.lower() else 'config/cball-parameters.json'
        self.param = AnalysisOption('param', pconf, particle)
        self.param.relaxed = r
        self.param.ispi0 = p

    @property
    def label(self):
        return self.pt.label

    @label.setter
    def label(self, label):
        self.pt.label = label

    @staticmethod
    def fixed_peak(*args):
        options = Options(*args)
        options.spectrum.fit_mass_width = False
        options.mode = 'd'
        return options


