import json
import ROOT
from recordclass import recordclass

PDG_BR_RATIO = {
    "#pi^{0}": 0.9882,
    "#eta": 0.3931,
}


def _option_hook(particle, ignore=("comment", "#pi^{0}", "#eta", "electrons")):
    def _hook(data):
        params = {k: v for k, v in data.iteritems() if k not in ignore}

        if particle in data:
            params = dict(params, **data[particle]._asdict())

        params["particle"] = particle
        return recordclass('AnalysisOption', params.keys())(*params.values())
    return _hook


def option(name, config, particle):
    with open(config) as f:
        conf = json.load(f, object_hook=_option_hook(particle))
    return conf


class AnalysisOption(object):
    _ignore_attributes = "#eta", "#pi^{0}", "comment", "electrons"

    _particles = {
        "pi0": "#pi^{0}",
        "eta": "#eta",
        "electrons": "electrons"
    }

    def __init__(self, name, config, particle):
        super(AnalysisOption, self).__init__()
        self._name = name
        self._config = config
        self.particle = particle
        with open(self._config) as f:
            conf = json.load(f)
        self._setup_configurations(conf, self.particle)

    def _setup_configurations(self, conf, particle):
        self._update_variables(conf)

        if particle not in conf:
            return

        conf = conf[particle]
        self._update_variables(conf)

    def _update_variables(self, vardict):
        items = (k for k in vardict if k not in self._ignore_attributes)
        for n in items:
            setattr(self, n, vardict[n])

    def __repr__(self):
        methods = ", ".join([s for s in dir(self) if not s.startswith('_')])
        msg = '{}("{}", "{}", "{}"): {}'
        return msg.format(
            self.__class__.__name__,
            self._name,
            self._config,
            self.particle,
            methods)


class Options(object):
    def __init__(self,
                 particle="#pi^{0}",
                 calibration="config/data/calibration.json",
                 pt="config/data/pt.json",
                 invmass="config/data/mass-fit.json",
                 signal="config/data/cball.json",
                 background="config/data/cball.json",
                 output="config/data/output.json",
                 ):
        super(Options, self).__init__()

        self.calibration = option("RangeEstimator", calibration, particle)
        self.pt = option("DataSlicer", pt, particle)
        self.output = option("DataExtractor", output, particle)
        self.invmass = option("MassFitter", invmass, particle)
        self.invmass.signal = AnalysisOption("signal", signal, particle)
        self.invmass.background = AnalysisOption("background",
                                                 background, particle)

        self.particle = particle


class OptionsSPMC(Options):

    def __init__(self,
                 particle="#pi^{0}",
                 pt="config/spmc/pt.json",
                 *args, **kwargs):
        super(OptionsSPMC, self).__init__(
            particle=particle,
            pt=pt,
            invmass="config/spmc/mass-fit.json",
            calibration="config/spmc/calibration.json",
            signal="config/spmc/cball.json",
            background="config/spmc/cball.json",
            *args, **kwargs)


class CompositeOptions(object):

    def __init__(self, particle, n_ranges=2,
                 pt="config/spmc/pt.json",
                 *args, **kwargs):
        super(CompositeOptions, self).__init__()
        options = [
            OptionsSPMC(particle, pt=pt, *args, **kwargs)
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
                 pt="config/data/pt.json",
                 otype=Options):
        super(EfficiencyOptions, self).__init__()
        genname = genname.format(particle)
        self.analysis = otype(particle=particle, pt=pt)
        self.genname = genname
        self.scale = scale

        histname = self.histpattern.format(particle=particle)
        self.decorate = "eff_" + particle, histname, "efficiency"


class CompositeEfficiencyOptions(object):

    def __init__(self, particle,
                 genname="hPt_{0}_primary_standard",
                 pt="config/spmc/pt.json",
                 use_particle=True,
                 scale=0.075, n_ranges=2, *args, **kwargs):
        super(CompositeEfficiencyOptions, self).__init__()
        self.suboptions = [
            EfficiencyOptions(
                particle=particle,
                genname=genname,
                pt=pt,
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

    def __init__(self, particle="#pi^{0}", pt="config/data/pt.json"):
        super(CorrectedYieldOptions, self).__init__()
        self.analysis = Options(particle=particle, pt=pt)
        self.analysis.output.scalew_spectrum = True
        self.spectrum = "spectrum"
        self.efficiency = EfficiencyOptions(
            particle=particle,
            genname="hPt_{0}_primary_standard",
            pt=pt
        )
        self.feeddown = FeeddownOptions(particle=particle)
        self.normalization = 1.
        self.branching_ratio = 1  # PDG_BR_RATIO.get(particle)

        self.decorate = {
            "histname": "corrected_yield",
            "title": self.histpattern.format(particle=particle),
            "label": particle,
            # "label": "ALICE, pp #sqrt{s} = 13 TeV",
        }


class CompositeCorrectedYieldOptions(object):

    histpattern = """
        Corrected {particle} yield; p_{{T}}, GeV/c;
        #frac{{1}}{{N_{{events}}}} #frac{{dN}}{{d p_{{T}}}}
    """

    def __init__(self, particle="#pi^{0}", n_ranges=2,
                 pt="config/pt-corrected.json"):
        super(CompositeCorrectedYieldOptions, self).__init__()
        self.analysis = Options(particle=particle, pt=pt)
        self.analysis.output.scalew_spectrum = True
        self.spectrum = "spectrum"
        self.efficiency = CompositeEfficiencyOptions(
            particle,
            n_ranges=n_ranges,
            pt=pt
        )
        self.feeddown = FeeddownOptions(particle=particle)
        self.decorate = {
            "histname": "corrected_yield",
            "title": self.histpattern.format(particle=particle),
            "label": particle,
            # "label": "ALICE, pp #sqrt{s} = 13 TeV",
        }
        self.normalization = 1.
        self.branching_ratio = 1  # PDG_BR_RATIO.get(particle)


# TODO: Add pt parameter to the feeddown
class FeeddownOptions(object):
    def __init__(self, particle="#pi^{0}"):
        super(FeeddownOptions, self).__init__()
        self.particle = particle
        self.feeddown = Options(particle=particle)
        # self.feeddown = Options(pt="config/pt-same.json")
        # NB: Don't fit the mass and width and
        #     use the same values from the data
        self.feeddown.calibration.mass.fit = False
        self.feeddown.calibration.width.fit = False
        self.regular = Options(particle=particle)
        # self.regular = Options(pt="config/pt-same.json")
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
        self.analysis = Options(pt="config/tag-and-probe-tof.json")
        # NB: Make sure to define it later
        self.fitfunc = None


class EpRatioOptions(object):
    def __init__(self):
        # We need only pT similar to the original analysis
        self.analysis = Options(
            particle="electrons",
            pt="config/ep_ratio/pt.json",
            calibration="config/ep_ratio/ep.json",
            background="config/ep_ratio/peak.json",
            signal="config/ep_ratio/peak.json",
            output="config/ep_ratio/output.json",
            invmass="config/ep_ratio/mass.json",
        )
        # NB: Make sure to define it later
        self.histname = "hEp_ele"
        self.fitf = ROOT.TF1("ratio", "pol0(0)", 0, 3)
        self.fitf.SetParameter(0, 1.0)


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
        pt = "config/pt-nonlinearity.json"

        self.data = Options(particle=particle, pt=pt)
        self.mc = CompositeOptions(particle, pt=pt, n_ranges=n_ranges)
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
            pt="config/spmc/pt.json")

        self.analysis_data = Options(
            particle=particle,
            pt="config/spmc/pt.json")
        self.factor = 1.
