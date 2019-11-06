import six
import tqdm
import joblib

import spectrum.broot as br
from spectrum.options import Options, CompositeCorrectedYieldOptions
from spectrum.options import CompositeEfficiencyOptions
from spectrum.corrected_yield import CorrectedYield
from spectrum.pipeline import TransformerBase
from spectrum.output import open_loggs
from spectrum.tools.feeddown import data_feeddown
from spectrum.plotter import plot
from vault.datavault import DataVault
import spectrum.sutils as su


memory = joblib.Memory('.joblib-cachedir', verbose=0)


def yield_extraction_data(particle="#pi^{0}"):
    production = "single {particle}".format(particle=particle)
    spmc_inputs = (
        DataVault().input(production, "low", "PhysEff"),
        DataVault().input(production, "high", "PhysEff"),
    )

    needs_feeddown = particle != "#pi^{0}"
    cyield = (
        (
            DataVault().input("data", histname="MassPtSM0"),
            data_feeddown(dummy=needs_feeddown),
        ),
        spmc_inputs
    )
    return cyield


@memory.cache()
def _calculate_yields(conf, data):
    print(conf)
    spectrums = {}
    pbar = tqdm.tqdm(
        total=len(conf.fit_range) *
        len(conf.backgrounds) *
        len(conf.signals) *
        len(conf.nsigmas)
    )
    cyield = CompositeCorrectedYieldOptions(conf.particle)
    for flab, frange in six.iteritems(conf.fit_range):
        for bckgr in conf.backgrounds:
            for marker, par in enumerate(conf.signals):
                for nsigmas in conf.nsigmas:
                    msg = "n#sigma = {} {} {} {}"
                    label = msg.format(nsigmas, par, bckgr, flab)

                    options = Options(
                        particle=conf.particle,
                        signal=conf.signals[par],
                        background=conf.signals[par]
                    )
                    options.calibration.dead = True
                    options.calibration.nsigmas = nsigmas
                    options.invmass.signal.background = bckgr
                    options.invmass.signal.fit_range = frange
                    options.invmass.background.fit_range = frange
                    options.invmass.signal.background = bckgr

                    cyield.analysis = options
                    cyield.efficiency = CompositeEfficiencyOptions(
                        particle=conf.particle,
                        signal=conf.signals[par],
                        background=conf.signals[par]
                    )
                    for eff in cyield.efficiency.suboptions:
                        eff.analysis.calibration.dead = True
                        eff.analysis.calibration.nsigmas = nsigmas
                        eff.analysis.invmass.signal.background = bckgr
                        eff.analysis.invmass.signal.fit_range = frange
                        eff.analysis.invmass.background.fit_range = frange
                        eff.analysis.invmass.signal.background = bckgr

                    with open_loggs() as loggs_local:
                        estimator = CorrectedYield(cyield)
                        spectrum = estimator.transform(data, loggs_local)
                        # loggs.update({label: loggs_local})
                    spectrum.marker = marker
                    print("Asigning the label", label)
                    spectrum.label = label
                    spectrum.logy = False
                    spectrums[label] = spectrum
                    pbar.update()
    pbar.close()
    return spectrums


class YieldExtractioinUncertanityOptions(object):
    _fit_ranges = {
        "#pi^{0}": {
            "low": [0.06, 0.22],
            "mid": [0.04, 0.20],
            "wide": [0.08, 0.24]
        },
        "#eta": {
            "low": [0.35, 0.65],
            "mid": [0.4, 0.7],
            "wide": [0.45, 0.78]
        },
    }

    def __init__(self, particle):
        self.fit_range = self._fit_ranges[particle]
        self.backgrounds = [
            "pol2",
            "pol1"
        ]
        self.signals = {
            "CrystalBall": "config/data/cball.json",
            "Gaus": "config/data/gaus.json",
        }
        self.nsigmas = [
            2,
            3
        ]
        self.particle = particle


class YieldExtractioin(TransformerBase):

    def __init__(self, options, plot=False):
        super(YieldExtractioin, self).__init__(plot)
        self.options = options
        self.plot = plot

    def transform(self, data, loggs):
        spectrums = _calculate_yields(self.options, data)
        for label, spectrum in six.iteritems(spectrums):
            spectrum.label = label
            spectrum.SetTitle(label)

        spectrums = list(spectrums.values())
        plot(
            spectrums,
            # xlimits=(0.8, 30.0),
            xtitle="p_{T} (GeV/#it{c})",
            # ytitle=invariant_cross_section_code(),
            csize=(96, 128),
            legend_pos=(0.72, 0.6, 0.88, 0.88),
            oname="results/systematics/yields/spectra-{}.pdf".format(
                su.spell(self.options.particle)),
            stop=self.plot,
            more_logs=False,
            yoffset=1.6,
            ltext_size=0.015
        )

        average = br.average(spectrums, "averaged yield")
        average.GetYaxis().SetTitle("average")
        plot(
            list(map(lambda x: br.ratio(x, average), spectrums)),
            # xlimits=(0.8, 30.0),
            logy=False,
            xtitle="p_{T} (GeV/#it{c})",
            # ytitle=spectrums[0] + ' / Average',
            csize=(96, 128),
            legend_pos=(0.72, 0.6, 0.88, 0.88),
            oname="results/systematics/yields/ratios-{}.pdf".format(
                su.spell(self.options.particle)),
            stop=self.plot,
            more_logs=False,
            yoffset=1.6,
            ltext_size=0.015
        )

        uncert, rms, mean = br.systematic_deviation(spectrums)
        uncert.logy = False
        loggs.update({"uncertainty": uncert})
        loggs.update({"rms": rms})
        loggs.update({"mean": mean})
        # uncert.SetTitle(
        #     "Systematic uncertanity from yield extraction (RMS/mean)")
        # diff = Comparator(stop=self.plot,
        #                   oname="syst-error-yield-extraction")
        # diff.compare(uncert)
        return uncert
