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
    def __init__(self, 
            particle='#pi^{0}',
            relaxedcb=False, 
            fitf='cball',
            spectrumconf='config/spectrum.json',
            ptrange='config/pt.json',
            outconf='config/spectrum-output.json',
            invmassconf='config/invariant-mass.json',
            backgroudpconf='config/cball-parameters.json',
            signalp='config/cball-parameters.json',
        ):
        super(Options, self).__init__()
        
        self.spectrum = AnalysisOption('RangeEstimator', spectrumconf, particle)
        self.pt = AnalysisOption('DataSlicer', ptrange, particle)
        self.output = AnalysisOption('DataExtractor', outconf, particle)

        self.backgroundp = AnalysisOption('backgroundp', backgroudpconf, particle)
        self.backgroundp.relaxed = relaxedcb

        self.signalp = AnalysisOption('signalp', signalp, particle)
        self.signalp.relaxed = relaxedcb

        self.invmass = AnalysisOption('MassFitter', invmassconf, particle)
        self.invmass.average = {}
        self.invmass.signalp = self.signalp
        self.invmass.backgroundp = self.backgroundp

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
        options = Options(
            particle=particle, 
            ptrange='config/pt-spmc.json',
            spectrumconf='config/spectrum_spmc.json',
            backgroudpconf='config/cball-parameters-spmc-test.json',
            signalp='config/cball-parameters-spmc-test.json'
        )
        options.spectrum.fit_range = pt_fit_range
        options.invmass.use_mixed = False
        return options


class EfficiencyOptions(object):

    def __init__(self, genname='hPt_#pi^{0}_primary_'):
        super(EfficiencyOptions, self).__init__()
        self.analysis = Options()
        self.genname = genname 

    @classmethod
    def spmc(klass, pt_range, particle="#pi^{0}"):
        efficiency_options = klass()
        efficiency_options.analysis = Options().spmc(pt_range, particle=particle)
        return efficiency_options


class MultirangeEfficiencyOptions(object):

    def __init__(self, effoptions, mergeranges):
        super(MultirangeEfficiencyOptions, self).__init__()
        self.suboptions = effoptions
        self.mergeranges = mergeranges

    @classmethod
    def spmc(klass, unified_input, particle):
        options = [EfficiencyOptions.spmc(rr, particle) for _, rr in unified_input.iteritems()]
        return klass(options, unified_input.values()) 

