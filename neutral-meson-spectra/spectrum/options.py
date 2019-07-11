import json
import ROOT

PDG_BR_RATIO = {
    "#pi^{0}": 0.9882,
    "#eta": 0.3931,
}


class AnalysisOption(object):
    ignore_attributes = "#eta", "#pi^{0}", "comment", "electrons"

    _particles = {
        "pi0": "#pi^{0}",
        "eta": "#eta",
        "electrons": "electrons"
    }

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
                 calibration="config/data/calibration.json",
                 ptrange="config/data/pt.json",
                 outconf="config/data/output.json",
                 invmassconf="config/data/mass-fit.json",
                 backgroudpconf="config/data/cball.json",
                 signalp="config/data/cball.json",
                 ):
        super(Options, self).__init__()

        self.calibration = AnalysisOption(
            "RangeEstimator", calibration, particle)

        self.pt = AnalysisOption("DataSlicer", ptrange, particle)
        self.output = AnalysisOption("DataExtractor", outconf, particle)
        self.output.scalew_spectrum = True

        self.backgroundp = AnalysisOption(
            "backgroundp", backgroudpconf, particle)

        self.signalp = AnalysisOption("signalp", signalp, particle)

        self.invmass = AnalysisOption("MassFitter", invmassconf, particle)
        self.invmass.signalp = self.signalp
        self.invmass.backgroundp = self.backgroundp

        self.particle = particle


class OptionsSPMC(Options):

    def __init__(self,
                 particle="#pi^{0}",
                 ptrange="config/spmc/pt.json",
                 *args, **kwargs):
        super(OptionsSPMC, self).__init__(
            particle=particle,
            ptrange=ptrange,
            calibration="config/spmc/calibration.json",
            backgroudpconf="config/spmc/cball.json",
            signalp="config/spmc/cball.json",
            *args, **kwargs)
        self.invmass.use_mixed = False


class CompositeOptions(object):

    def __init__(self, particle, n_ranges=2,
                 ptrange="config/spmc/pt.json",
                 *args, **kwargs):
        super(CompositeOptions, self).__init__()
        options = [
            OptionsSPMC(particle, ptrange=ptrange, *args, **kwargs)
            for _ in range(n_ranges)
        ]

        names = ["{0}".format(rr) for rr in range(n_ranges)]
        self.steps = zip(names, options)

        self.mergeranges = [(0.0, 7.0), (7.0, 20.0)]
        if particle == "#eta":
            self.mergeranges = [(0.0, 6.0), (6.0, 20.0)]


class EfficiencyOptions(object):

    histpattern = """
    #varepsilon = #Delta #phi #Delta y/ 2 #pi
    #frac{{Number of reconstructed {particle}}}
    {{Number of generated primary {particle}}}
    ; p_{{T}}, GeV/c; efficiency #times acceptance
    """

    def __init__(self, particle="#pi^{0}",
                 genname="hPt_{0}_primary_standard",
                 scale=0.075,
                 ptrange="config/data/pt.json",
                 otype=Options):
        super(EfficiencyOptions, self).__init__()
        genname = genname.format(particle)
        self.analysis = otype(particle=particle, ptrange=ptrange)
        self.genname = genname
        self.scale = scale

        histname = self.histpattern.format(particle=particle)
        self.decorate = "eff_" + particle, histname, "efficiency"


class CompositeEfficiencyOptions(object):

    def __init__(self, particle,
                 genname="hPt_{0}_primary_standard",
                 ptrange="config/spmc/pt.json",
                 use_particle=True,
                 scale=0.075, n_ranges=2, *args, **kwargs):
        super(CompositeEfficiencyOptions, self).__init__()
        self.suboptions = [
            EfficiencyOptions(
                particle=particle,
                genname=genname,
                ptrange=ptrange,
                scale=scale,
                otype=OptionsSPMC,
                *args, **kwargs)
            for _ in range(n_ranges)
        ]
        self.mergeranges = [(0.0, 7.0), (7.0, 20.0)]
        if len(self.suboptions[0].analysis.pt.ptedges) <= 14:  # eta size
            self.mergeranges = [(0.0, 6.0), (6.0, 20.0)]

        self.analysis = CompositeOptions(particle)
        self.reduce_function = "standard"


class CorrectedYieldOptions(object):

    histpattern = """
        Corrected {particle} yield; p_{{T}}, GeV/c;
        #frac{{1}}{{N_{{events}}}} #frac{{dN}}{{d p_{{T}}}}}}
    """

    def __init__(self, particle="", ptrange="config/data/pt.json"):
        super(CorrectedYieldOptions, self).__init__()
        self.analysis = Options(particle=particle, ptrange=ptrange)
        self.analysis.output.scalew_spectrum = True
        self.spectrum = "spectrum"
        self.efficiency = EfficiencyOptions(
            particle=particle,
            genname="hPt_{0}_primary_standard",
            ptrange=ptrange
        )
        self.feeddown = FeeddownOptions(particle=particle)
        self.normalization = 1.
        self.branching_ratio = 1  # PDG_BR_RATIO.get(particle)

        self.decorate = {
            "histname": "corrected_yield",
            "title": self.histpattern.format(particle=particle),
            "label": "ALICE, pp #sqrt{s} = 13 TeV",
        }


class CompositeCorrectedYieldOptions(object):

    histpattern = """
        Corrected {particle} yield; p_{{T}}, GeV/c;
        #frac{{1}}{{N_{{events}}}} #frac{{dN}}{{d p_{{T}}}}
    """

    def __init__(self, particle="", n_ranges=2,
                 ptrange="config/pt-corrected.json"):
        super(CompositeCorrectedYieldOptions, self).__init__()
        self.analysis = Options(particle=particle, ptrange=ptrange)
        self.analysis.output.scalew_spectrum = True
        self.spectrum = "spectrum"
        self.efficiency = CompositeEfficiencyOptions(
            particle,
            n_ranges=n_ranges,
            ptrange=ptrange
        )
        self.feeddown = FeeddownOptions(particle=particle)
        self.decorate = {
            "histname": "corrected_yield",
            "title": self.histpattern.format(particle=particle),
            "label": "ALICE, pp #sqrt{s} = 13 TeV",
        }
        self.normalization = 1.
        self.branching_ratio = 1  # PDG_BR_RATIO.get(particle)


# TODO: Add ptrange parameter to the feeddown
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
            ptrange="config/ep_ratio/pt.json",
            calibration="config/ep_ratio/ep.json",
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
            ptrange="config/spmc/pt.json")
        self.analysis_data = Options(ptrange="config/spmc/pt.json")
        self.factor = 1.
