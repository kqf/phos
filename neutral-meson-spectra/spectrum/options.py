#!/usr/bin/python
import json


class AnalysisOption(object):
    ignore_attributes = '#eta', '#pi^{0}', 'comment'
    _particles = {"pi0": "#pi^{0}", "eta": "#eta"}

    def __init__(self, name, config, particle):
        super(AnalysisOption, self).__init__()
        self.name = name
        self.particle = self._convert_name(particle)
        with open(config) as f:
            conf = json.load(f)
        self._setup_configurations(conf, self.particle)

    def _setup_configurations(self, conf, particle):
        self._update_variables(conf)

        if particle not in conf:
            return

        conf = conf[particle]
        self._update_variables(conf)

    def _update_variables(self, vardict):
        items = (k for k in vardict if k not in self.ignore_attributes)
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

        self.spectrum = AnalysisOption(
            'RangeEstimator', spectrumconf, particle)
        self.pt = AnalysisOption('DataSlicer', ptrange, particle)
        self.output = AnalysisOption('DataExtractor', outconf, particle)
        self.output.scalew_spectrum = False

        self.backgroundp = AnalysisOption(
            'backgroundp', backgroudpconf, particle)
        self.backgroundp.relaxed = relaxedcb

        self.signalp = AnalysisOption('signalp', signalp, particle)
        self.signalp.relaxed = relaxedcb

        self.invmass = AnalysisOption('MassFitter', invmassconf, particle)
        self.invmass.signalp = self.signalp
        self.invmass.backgroundp = self.backgroundp

        self.particle = particle

    @property
    def fitf(self):
        return self.backgroundp.fitf

    @fitf.setter
    def fitf(self, fitf):
        # This one is needed only for. systematic error estimation
        #
        relaxed, particle = self.backgroundp.relaxed, self.backgroundp.particle
        prefix = 'gaus' if 'gaus' in fitf.lower() else 'cball'
        pconf = 'config/{0}-parameters.json'.format(prefix)
        self.backgroundp = AnalysisOption('backgroundp', pconf, particle)
        self.backgroundp.relaxed = relaxed

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
        rebins = [0 for i in range(len(edges) - 1)]
        rebins[-1] = 3
        rebins[-2] = 3
        options.pt.ptedges = edges
        options.pt.rebins = rebins
        return options

    @staticmethod
    def spmc(pt_fit_range, particle='pi0',
             ptrange='config/pt-spmc.json', *args, **kwargs):
        options = Options(
            particle=particle,
            ptrange=ptrange,
            spectrumconf='config/spectrum-spmc.json',
            backgroudpconf='config/cball-parameters-spmc-enhanced.json',
            signalp='config/cball-parameters-spmc-signal.json',
            *args,
            **kwargs
        )
        options.spectrum.fit_range = pt_fit_range
        options.invmass.use_mixed = False
        return options


class OptionsSPMC(Options):
    def __init__(self, pt_fit_range,
                 particle='#pi^{0}',
                 ptrange='config/pt-spmc.json',
                 spectrumconf='config/spectrum-spmc.json',
                 backgroudpconf='config/cball-parameters-spmc-enhanced.json',
                 signalp='config/cball-parameters-spmc-signal.json',
                 *args,
                 **kwargs
                 ):
        super(OptionsSPMC, self).__init__(ptrange=ptrange,
                                          particle=particle,
                                          spectrumconf=spectrumconf,
                                          signalp=signalp,
                                          *args, **kwargs)
        self.spectrum.fit_range = pt_fit_range
        self.invmass.use_mixed = False


class CompositeOptions(object):

    def __init__(self, unified_inputs, particle, *args, **kwargs):
        super(CompositeOptions, self).__init__()
        self.mergeranges = [rr for rr in unified_inputs.values()]
        options = [Options.spmc(rr, particle, *args, **kwargs)
                   for rr in self.mergeranges]
        names = ["{0}-{1}".format(*rr) for rr in self.mergeranges]
        self.steps = zip(names, options)


class EfficiencyOptions(object):

    def __init__(self, particle='#pi^{0}',
                 genname='hPt_#pi^{0}_primary_standard',
                 scale=0.075,
                 ptrange="config/pt.json"):
        super(EfficiencyOptions, self).__init__()
        self.analysis = Options(particle=particle, ptrange=ptrange)
        self.genname = genname
        self.scale = scale

        histname = "#varepsilon = #Delta #phi #Delta y/ 2 #pi "
        histname += "#frac{Number of reconstructed %s}" % particle
        histname += "{Number of generated primary %s}" % particle
        histname += "; p_{T}, GeV/c; efficiency #times acceptance"
        self.decorate = "eff_" + particle, histname

    def set_binning(self, ptedges, rebins):
        self.analysis.pt.ptedges = ptedges
        self.analysis.pt.rebins = rebins

    @classmethod
    def spmc(klass, pt_range, particle="#pi^{0}",
             genname='hPt_#pi^{0}_primary_standard', *args, **kwargs):
        efficiency_options = klass(genname=genname)
        efficiency_options.analysis = Options().spmc(
            pt_range, particle=particle, *args, **kwargs)
        return efficiency_options


class CompositeEfficiencyOptions(object):

    def __init__(self, unified_inputs, particle,
                 genname='hPt_{0}_primary_standard',
                 use_particle=True, *args, **kwargs):
        super(CompositeEfficiencyOptions, self).__init__()
        if use_particle:
            genname = genname.format(particle)
        self.suboptions = [EfficiencyOptions.spmc(
            rr, particle, genname, *args, **kwargs)
            for _, rr in unified_inputs.iteritems()
        ]
        self.mergeranges = unified_inputs.values()

    def set_binning(self, ptedges, rebins):
        for eff_options in self.suboptions:
            eff_options.analysis.pt.ptedges = ptedges
            eff_options.analysis.pt.rebins = rebins

    @classmethod
    def spmc(klass, unified_inputs, particle,
             genname='hPt_{0}_primary_standard',
             use_particle=True, *args, **kwargs):
        if use_particle:
            genname = genname.format(particle)
        options = [EfficiencyOptions.spmc(
            rr, particle, genname, *args, **kwargs)
            for _, rr in unified_inputs.iteritems()
        ]
        return klass(options, unified_inputs.values())


class CorrectedYieldOptions(object):
    def __init__(self, particle=""):
        super(CorrectedYieldOptions, self).__init__()
        self.analysis = Options(particle=particle)
        self.analysis.output.scalew_spectrum = True
        self.spectrum = "spectrum"
        self.efficiency = EfficiencyOptions(
            genname='hPt_{0}_primary_'.format(particle))

    def set_binning(self, ptedges, rebins):
        self.analysis.pt.ptedges = ptedges
        self.analysis.pt.rebins = rebins
        self.efficiency.set_binning(ptedges, rebins)


class CompositeCorrectedYieldOptions(object):
    def __init__(self, particle="", unified_inputs=None):
        super(CompositeCorrectedYieldOptions, self).__init__()
        self.analysis = Options(
            particle=particle,
            ptrange="config/pt-corrected.json"
        )
        self.analysis.output.scalew_spectrum = True
        self.spectrum = "spectrum"
        self.efficiency = CompositeEfficiencyOptions(unified_inputs, particle)

    def set_binning(self, ptedges, rebins):
        self.analysis.pt.ptedges = ptedges
        self.analysis.pt.rebins = rebins
        self.efficiency.set_binning(ptedges, rebins)


class FeeddownOptions(object):
    def __init__(self):
        super(FeeddownOptions, self).__init__()
        self.feeddown = Options()
        # self.feeddown = Options(ptrange='config/pt-same.json')
        # NB: Don't fit the mass and width and
        #     use the same values from the data
        self.feeddown.spectrum.fit_mass_width = False
        self.regular = Options()
        # self.regular = Options(ptrange='config/pt-same.json')
        # NB: Make sure to define and assign the feeddown parametrization
        self.fitf = None


class ProbeTofOptions(object):
    def __init__(self):
        self.analysis = Options(ptrange='config/tag-and-probe-tof.json')
        # NB: Make sure to define it later
        self.fitfunc = None


class EpRatioOptions(object):
    def __init__(self):
        # We need only pT similar to the original analysis
        self.pt = Options().pt
        # NB: Make sure to define it later
        self.histname = 'hEpElectronsPSM0'


class NonlinearityOptions(object):

    def __init__(self):
        super(NonlinearityOptions, self).__init__()
        self.data = Options()
        self.mc = Options()
        # NB: Don't assingn to get an exception
        self.fitf = None
        self.decorate = self.data.particle, "Nonlinearity"


class CompositeNonlinearityOptions(object):

    def __init__(self, unified_inputs, particle="#pi^{0}"):
        super(CompositeNonlinearityOptions, self).__init__()
        ptrange = "config/pt-nonlinearity.json"

        self.data = Options(ptrange=ptrange)
        self.mc = CompositeOptions(unified_inputs, particle, ptrange=ptrange)
        # NB: Don't assingn to get an exception
        self.fitf = None
        self.decorate = self.data.particle, "Nonlinearity"


class NonlinearityScanOptions(object):

    def __init__(self, nbins=11):
        super(NonlinearityScanOptions, self).__init__()
        self.nbins = nbins
        self.analysis = Options()
