#!/usr/bin/python


import json


class AnalysisOption(object):
    ignore_attributes = 'eta', 'pi0', 'comment'
    _particles = {"#pi^{0}": "pi0", "#eta": "eta"}

    def __init__(self, name, config, particle):
        super(AnalysisOption, self).__init__()
        self.name = name
        self.particle = self._convert_name(particle)
        with open(config) as f:
            conf = json.load(f)
        self._setup_configurations(conf, self.particle)


    def _setup_configurations(self, conf, particle):
        self._update_variables(conf)

        if not particle in conf:
            return

        conf = conf[particle]
        self._update_variables(conf)


    def _update_variables(self, vardict):
        items = (k for k in vardict if not k in self.ignore_attributes)
        for n in items:
            setattr(self, n, vardict[n])

    @classmethod
    def _convert_name(klass, name):
        if name not in klass._particles:
            return name

        cleaned = klass._particles.get(name)
        return cleaned




class Options(object):
    """
        This is class should handle all possible variable! options 
        that i need to compare in my analysis.
    """
    modes = {'quiet': False, 'q': False , 'silent': False, 's': False, 'dead': False, 'd': False}

    def __init__(self, label = 'data', mode = 'q', relaxedcb = False, 
                    particle='pi0', priority = 999, fitf = 'cball',
                    spectrumconf = 'config/spectrum.json',
                    ptrange = 'config/pt.json',
                    ptconf = 'config/pt-analysis.json',
                    invmassconf = 'config/invariant-mass.json',
                    paramconf = 'config/cball-parameters.json',
                    spmc = False):

        super(Options, self).__init__()
        show_img = self.modes.get(mode, True)

        self.spectrum = AnalysisOption('spectrum', spectrumconf, particle)
        self.spectrum.show_img = show_img


        self.pt = AnalysisOption('ptanalysis', ptrange, particle)

        self.output = AnalysisOption('ptanalysis', ptconf, particle)
        self.output.priority = priority
        self.output.label = label
        self.output.show_img = show_img
        self.output.dead_mode = 'd' in mode
        self.output.particle = particle

        self.invmass = AnalysisOption('invmass', invmassconf, particle)
        self.invmass.average = {}

        self.param = AnalysisOption('param', paramconf, particle)
        self.param.relaxed = relaxedcb
        self.particle = particle

    @property
    def fitf(self):
        return self.param.fitf

    @fitf.setter
    def fitf(self, fitf):
        relaxed, particle = self.param.relaxed, self.param.particle 
        prefix = 'gaus' if 'gaus' in fitf.lower() else 'cball'
        pconf = 'config/{0}-parameters.json'.format(prefix)
        self.param = AnalysisOption('param', pconf, particle)
        self.param.relaxed = relaxed

    @property
    def label(self):
        return self.output.label

    @label.setter
    def label(self, label):
        self.output.label = label

    @staticmethod
    def fixed_peak(*args):
        options = Options(*args)
        options.spectrum.fit_mass_width = False
        options.mode = 'd'
        return options

    @staticmethod
    def coarse_binning(options):
        edges = options.pt.ptedges
        edges = [e for e in edges if int(10 * e) % 10 != 5]
        rebins = [0 for i in range(len(edges) -1)]
        rebins[-1] = 3
        rebins[-2] = 3
        options.pt.ptedges = edges
        options.pt.rebins = rebins
        return options

    @staticmethod
    def spmc(pt_fit_range, label = '', particle = 'pi0'):
        name = '%.4g < p_{T} < %.4g' % pt_fit_range
        options = Options(name,
                    mode = 'q', 
                    particle = particle, 
                    ptrange = 'config/pt-spmc.json',
                    spectrumconf = 'config/spectrum_spmc.json',
                    paramconf = 'config/cball-parameters-spmc-test.json'
        )

        options.spectrum.fit_range = pt_fit_range

        if label:
            options.label = label 

        return options