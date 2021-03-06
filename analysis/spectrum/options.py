import ROOT

import json
import six

from recordclass import recordclass

MERGERANGES = {
    "#pi^{0}": [(0.0, 7.0), (7.0, 20.0)],
    "#eta": [(0.0, 7.0), (7.0, 20.0)],
}


def _option_hook(particle, ignore=("comment", "#pi^{0}", "#eta", "electrons")):
    def _hook(data):
        params = {k: v for k, v in six.iteritems(data) if k not in ignore}

        if particle in data:
            params = dict(params, **data[particle]._asdict())

        params["particle"] = particle
        return recordclass('AnalysisOption', params.keys())(*params.values())
    return _hook


def option(config, particle):
    with open(config) as f:
        conf = json.load(f, object_hook=_option_hook(particle))
    return conf


class Options(object):
    def __init__(
        self,
        particle="#pi^{0}",
        pt="config/pt.json",
        calibration="config/data/calibration.json",
        invmass="config/data/mass-fit.json",
        signal="config/data/cball.json",
        background="config/data/cball.json",
        output="config/data/output.json",
    ):
        super(Options, self).__init__()
        self.calibration = option(calibration, particle)
        self.pt = option(pt, particle)
        self.output = option(output, particle)
        self.invmass = option(invmass, particle)
        self.invmass.signal = option(signal, particle)
        self.invmass.background = option(background, particle)
        self.particle = particle


class OptionsSPMC(Options):

    def __init__(
            self,
            particle="#pi^{0}",
            pt="config/pt.json",
            calibration="config/spmc/calibration.json",
            invmass="config/spmc/mass-fit.json",
            signal="config/spmc/cball.json",
            background="config/spmc/cball.json",
            *args, **kwargs
    ):
        super(OptionsSPMC, self).__init__(
            particle=particle,
            pt=pt,
            calibration=calibration,
            invmass=invmass,
            signal=signal,
            background=background,
            *args, **kwargs)


class CompositeOptions(object):
    def __init__(
            self, particle, n_ranges=2,
            pt="config/pt.json",
            *args, **kwargs):
        super(CompositeOptions, self).__init__()
        options = [
            OptionsSPMC(particle, pt=pt, *args, **kwargs)
            for _ in range(n_ranges)
        ]

        names = ["{0}".format(rr) for rr in range(n_ranges)]
        self.steps = list(zip(names, options))
        self.mergeranges = MERGERANGES[particle]
        self.particle = particle


class EfficiencyOptions(object):

    histpattern = (
        "; #it{{p}}_{{T}} (GeV/#it{{c}})"
        "; #varepsilon #times #it{{A}}"
    )

    def __init__(
        self, particle="#pi^{0}",
        scale=0.075,
        pt="config/pt.json",
        otype=Options,
        **kwargs
    ):
        super(EfficiencyOptions, self).__init__()
        self.analysis = otype(particle=particle, pt=pt, **kwargs)
        self.scale = scale
        self.decorate = {
            "histname": "eff_{}".format(particle),
            "title": self.histpattern.format(particle=particle),
            "label": "efficiency",
        }


class CompositeEfficiencyOptions(object):
    def __init__(
            self, particle,
            pt="config/pt.json",
            use_particle=True,
            scale=0.075,
            n_ranges=2,
            *args, **kwargs
    ):
        super(CompositeEfficiencyOptions, self).__init__()
        self.suboptions = [
            EfficiencyOptions(
                particle=particle,
                pt=pt,
                scale=scale,
                otype=OptionsSPMC,
                *args, **kwargs)
            for _ in range(n_ranges)
        ]
        self.mergeranges = MERGERANGES[particle]
        if len(self.suboptions[0].analysis.pt.ptedges) <= 14:  # eta size
            self.mergeranges = [(0.0, 6.0), (6.0, 20.0)]
        self.analysis = CompositeOptions(particle)
        self.reduce_function = "standard"


class CorrectedYieldOptions(object):

    histpattern = (
        "corrected {particle} yield;"
        "#it{{p}}_{{T}} (GeV/#it{{c}});"
        "#frac{{1}}{{#it{{N}}_{{events}}}} "
        "#frac{{d#it{{N}}}}{{d #it{{p}}_{{T}}}}"
    )

    def __init__(self, particle="#pi^{0}", pt="config/pt.json"):
        super(CorrectedYieldOptions, self).__init__()
        self.analysis = Options(particle=particle, pt=pt)
        self.analysis.output.scalew_spectrum = True
        self.spectrum = "spectrum"
        self.efficiency = EfficiencyOptions(particle=particle, pt=pt)
        self.feeddown = FeeddownOptions(particle=particle)
        self.normalization = 1.
        self.branching_ratio = 1  # PDG_BR_RATIO.get(particle)

        self.decorate = {
            "histname": "corrected_yield",
            "title": self.histpattern.format(particle=particle),
            "label": particle,
        }


class CompositeCorrectedYieldOptions(object):

    histpattern = (
        "corrected {particle} yield;"
        "#it{{p}}_{{T}} (GeV/#it{{c}});"
        "#frac{{1}}{{#it{{N}}_{{events}}}} "
        "#frac{{d#it{{N}}}}{{d #it{{p}}_{{T}}}}"
    )

    def __init__(self, particle="#pi^{0}", n_ranges=2, pt="config/pt.json"):
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
            # "label": "ALICE, pp #sqrt{#it{s}} = 13 TeV",
        }
        self.normalization = 1.
        self.branching_ratio = 1  # PDG_BR_RATIO.get(particle)


class FeeddownOptions(object):
    def __init__(self, pt="config/pt.json", stop=False, particle="#pi^{0}"):
        super(FeeddownOptions, self).__init__()
        self.particle = particle
        self.feeddown = Options(pt=pt, particle=particle)
        self.feeddown.invmass.clean_empty_bins = False
        self.feeddown.invmass.use_mixed = False
        # NB: Don't fit the mass and width and
        #     use the same values from the data
        # self.feeddown.calibration.mass.fit = False
        # self.feeddown.calibration.width.fit = False
        self.regular = Options(pt=pt, particle=particle)
        # self.regular = Options(pt="config/pt-same.json")
        # NB: Make sure to define and assign the feeddown parametrization
        self.fitf = self.feeddown_paramerization()
        # Use the idendity transformation by default
        self.plot_func = lambda x, loggs: x
        # Ensure the right pT binning for the final particle histogram
        self.pt = Options(particle=particle).pt.ptedges
        self.stop = stop

    @staticmethod
    def feeddown_paramerization():
        func_feeddown = ROOT.TF1(
            "func_feeddown",
            "[2] * (1 + [0]*TMath::Exp(-x * x / [1] / [1] / 2))",
            0.8, 10
        )
        func_feeddown.SetParNames("A", "Sigma", "Scale")
        func_feeddown.FixParameter(0, 0.453)
        func_feeddown.FixParameter(1, 1.35)
        func_feeddown.FixParameter(2, 0.0478)
        return func_feeddown


class ProbeTofOptions(object):
    def __init__(self):
        self.analysis = Options(pt="config/tag-and-probe-tof.json")
        self.title = "Data; #it{E}_{#gamma} (GeV); #varepsilon_{TOF}"
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
        pt = "config/pt.json"

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
            pt="config/pt.json")

        self.analysis_data = Options(
            particle=particle,
            pt="config/pt.json")
        self.factor = 1.
