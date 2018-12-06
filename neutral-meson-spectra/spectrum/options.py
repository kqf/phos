#!/usr/bin/python
import json
import ROOT


class AnalysisOption(object):
    ignore_attributes = "#eta", "#pi^{0}", "comment", "electrons"
    _particles = {"pi0": "#pi^{0}", "eta": "#eta", "electrons": "electrons"}

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
                 particle="#pi^{0}",
                 fitrange=(0, 20.),  # Leave it for backward compatibility
                 relaxedcb=False,
                 fitf="cball",
                 spectrumconf="config/spectrum.json",
                 ptrange="config/pt.json",
                 outconf="config/spectrum-output.json",
                 invmassconf="config/invariant-mass.json",
                 backgroudpconf="config/cball-parameters.json",
                 signalp="config/cball-parameters.json",
                 ):
        super(Options, self).__init__()

        self.spectrum = AnalysisOption(
            "RangeEstimator", spectrumconf, particle)
        self.spectrum.ptrange = fitrange
        self.spectrum.fit_range = fitrange

        self.pt = AnalysisOption("DataSlicer", ptrange, particle)
        self.output = AnalysisOption("DataExtractor", outconf, particle)
        self.output.scalew_spectrum = True
        self.output.ptrange = fitrange

        self.backgroundp = AnalysisOption(
            "backgroundp", backgroudpconf, particle)
        self.backgroundp.relaxed = relaxedcb

        self.signalp = AnalysisOption("signalp", signalp, particle)
        self.signalp.relaxed = relaxedcb

        self.invmass = AnalysisOption("MassFitter", invmassconf, particle)
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
        prefix = "gaus" if "gaus" in fitf.lower() else "cball"
        pconf = "config/{0}-parameters.json".format(prefix)
        self.backgroundp = AnalysisOption("backgroundp", pconf, particle)
        self.backgroundp.relaxed = relaxed

    @staticmethod
    def fixed_peak(*args):
        options = Options(*args)
        options.spectrum.fit_mass_width = False
        options.mode = "d"
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
    def spmc(particle="#pi^{0}",
             ptrange="config/pt-spmc.json", *args, **kwargs):
        options = Options(
            particle=particle,
            ptrange=ptrange,
            spectrumconf="config/spectrum-spmc.json",
            backgroudpconf="config/cball-parameters-spmc.json",
            signalp="config/cball-parameters-spmc.json",
            *args,
            **kwargs
        )
        options.invmass.use_mixed = False
        return options


class CompositeOptions(object):

    def __init__(self, particle, n_ranges=2, *args, **kwargs):
        super(CompositeOptions, self).__init__()
        options = [
            Options.spmc(particle, *args, **kwargs)
            for _ in range(n_ranges)
        ]

        names = ["{0}".format(rr) for rr in range(n_ranges)]
        self.steps = zip(names, options)

        self.mergeranges = [(0.0, 7.0), (7.0, 20.0)]
        if particle == "#eta":
            self.mergeranges = [(0.0, 6.0), (6.0, 20.0)]


class EfficiencyOptions(object):

    def __init__(self, particle="#pi^{0}",
                 genname="hPt_#pi^{0}_primary_",
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
        self.decorate = "eff_" + particle, histname, "efficiency"

    def set_binning(self, ptedges, rebins):
        self.analysis.pt.ptedges = ptedges
        self.analysis.pt.rebins = rebins

    @classmethod
    def spmc(klass, particle="#pi^{0}",
             genname="hPt_#pi^{0}_primary_", scale=0.075,
             *args, **kwargs):
        efficiency_options = klass(genname=genname, scale=scale)
        efficiency_options.analysis = Options().spmc(
            particle=particle, *args, **kwargs)
        return efficiency_options


class CompositeEfficiencyOptions(object):

    def __init__(self, particle,
                 genname="hPt_{0}_primary_standard",
                 use_particle=True,
                 scale=0.075, n_ranges=2, *args, **kwargs):
        super(CompositeEfficiencyOptions, self).__init__()
        if use_particle:
            genname = genname.format(particle)
        self.suboptions = [
            EfficiencyOptions.spmc(
                particle=particle,
                genname=genname,
                scale=scale,
                *args, **kwargs)
            for _ in range(n_ranges)
        ]
        self.mergeranges = [(0.0, 7.0), (7.0, 20.0)]
        if particle == "#eta":
            self.mergeranges = [(0.0, 6.0), (6.0, 20.0)]

        self.analysis = CompositeOptions(particle)
        self.reduce_function = "standard"

    def set_binning(self, ptedges, rebins):
        for eff_options in self.suboptions:
            eff_options.analysis.pt.ptedges = ptedges
            eff_options.analysis.pt.rebins = rebins


class CorrectedYieldOptions(object):
    def __init__(self, particle=""):
        super(CorrectedYieldOptions, self).__init__()
        self.analysis = Options(particle=particle)
        self.analysis.output.scalew_spectrum = True
        self.spectrum = "spectrum"
        self.efficiency = EfficiencyOptions(
            genname="hPt_{0}_primary_".format(particle))
        self.feeddown = FeeddownOptions(particle=particle)

        out_title = "Corrected {} yield;".format(particle)
        out_title += " p_{T}, GeV/c;"
        out_title += "#frac{1}{N_{events}} #frac{dN}{d p_{T}}}"
        self.decorate = {
            "histname": "corrected_yield",
            "title": out_title,
            "label": "ALICE, pp \sqrt{s} = 13 TeV",
        }

    def set_binning(self, ptedges, rebins):
        self.analysis.pt.ptedges = ptedges
        self.analysis.pt.rebins = rebins
        self.efficiency.set_binning(ptedges, rebins)


class CompositeCorrectedYieldOptions(object):
    def __init__(self, particle="", n_ranges=2):
        super(CompositeCorrectedYieldOptions, self).__init__()
        self.analysis = Options(
            particle=particle,
            ptrange="config/pt-corrected.json"
        )
        self.analysis.output.scalew_spectrum = True
        self.spectrum = "spectrum"
        self.efficiency = CompositeEfficiencyOptions(
            particle,
            n_ranges=n_ranges
        )
        self.feeddown = FeeddownOptions(particle=particle)

        out_title = "Corrected {} yield;".format(particle)
        out_title += " p_{T}, GeV/c;"
        out_title += "#frac{1}{N_{events}} #frac{dN}{d p_{T}}"
        self.decorate = {
            "histname": "corrected_yield",
            "title": out_title,
            "label": "ALICE, pp \sqrt{s} = 13 TeV",
        }

    def set_binning(self, ptedges, rebins):
        self.analysis.pt.ptedges = ptedges
        self.analysis.pt.rebins = rebins
        self.efficiency.set_binning(ptedges, rebins)


class FeeddownOptions(object):
    def __init__(self, particle="#pi^{0}"):
        super(FeeddownOptions, self).__init__()
        self.particle = particle
        self.feeddown = Options(particle=particle)
        # self.feeddown = Options(ptrange="config/pt-same.json")
        # NB: Don"t fit the mass and width and
        #     use the same values from the data
        self.feeddown.spectrum.fit_mass_width = False
        self.regular = Options(particle=particle)
        # self.regular = Options(ptrange="config/pt-same.json")
        # NB: Make sure to define and assign the feeddown parametrization
        self.fitf = self.feeddown_paramerization()

    @staticmethod
    def feeddown_paramerization():
        func_feeddown = ROOT.TF1(
            "func_feeddown",
            "[2] * (1.+[0]*TMath::Exp(-x/2*x/2/2./[1]/[1]))",
            0, 100
        )
        func_feeddown.SetParNames("A", "#sigma", "E_{scale}")
        func_feeddown.SetParameter(0, -1.4)
        func_feeddown.SetParameter(1, 0.33)
        func_feeddown.SetParLimits(1, 0, 10)
        func_feeddown.SetParameter(2, 0.02)
        return func_feeddown


class ProbeTofOptions(object):
    def __init__(self):
        self.analysis = Options(ptrange="config/tag-and-probe-tof.json")
        # NB: Make sure to define it later
        self.fitfunc = None


class EpRatioOptions(object):
    def __init__(self):
        # We need only pT similar to the original analysis
        self.analysis = Options(
            particle="electrons",
            fitf="gaus",
            ptrange="config/ep_ratio/pt.json",
            spectrumconf="config/ep_ratio/ep.json",
            backgroudpconf="config/ep_ratio/peak.json",
            signalp="config/ep_ratio/peak.json",
            outconf="config/ep_ratio/output.json",
            invmassconf="config/ep_ratio/mass.json",
        )
        # NB: Make sure to define it later
        self.histname = "hEp_ele"


class DataMCEpRatioOptions(object):
    def __init__(self):
        self.data = EpRatioOptions()
        self.mc = EpRatioOptions()


class NonlinearityOptions(object):

    def __init__(self):
        super(NonlinearityOptions, self).__init__()
        self.data = Options()
        self.mc = Options()
        # NB: Don"t assingn to get an exception
        self.fitf = None
        self.decorate = self.data.particle, "Nonlinearity"
        self.factor = 1.0


class CompositeNonlinearityOptions(object):

    def __init__(self, particle="#pi^{0}", n_ranges=2):
        super(CompositeNonlinearityOptions, self).__init__()
        ptrange = "config/pt-nonlinearity.json"

        self.data = Options(particle=particle, ptrange=ptrange)
        self.mc = CompositeOptions(particle,
                                   ptrange=ptrange, n_ranges=n_ranges)
        # NB: Don"t assingn to get an exception
        self.fitf = None
        self.decorate = self.data.particle, "Nonlinearity"
        self.factor = 1.0


class NonlinearityScanOptions(object):

    def __init__(self, nbins=11):
        super(NonlinearityScanOptions, self).__init__()
        self.nbins = nbins
        self.analysis = Options()
        self.analysis_data = Options()
        self.factor = 1.


class CompositeNonlinearityScanOptions(object):

    def __init__(self, particle="#pi^{0}", nbins=11, n_ranges=2):
        super(CompositeNonlinearityScanOptions, self).__init__()
        self.nbins = nbins
        self.analysis = CompositeOptions(
            particle,
            n_ranges=n_ranges,
            ptrange="config/pt-spmc.json")
        self.analysis_data = Options(ptrange="config/pt-spmc.json")
        self.factor = 1.


class CompositeNonlinearityUncertainty(object):

    def __init__(self, particle="#pi^{0}", nbins=11, n_ranges=2):
        super(CompositeNonlinearityUncertainty, self).__init__()
        self.nbins = nbins
        self.eff = CompositeEfficiencyOptions(particle)
