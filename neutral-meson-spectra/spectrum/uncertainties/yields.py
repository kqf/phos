import six
import tqdm
from spectrum.broot import BROOT as br
from spectrum.options import Options
from spectrum.comparator import Comparator
from spectrum.corrected_yield import CorrectedYield
from spectrum.pipeline import TransformerBase
from spectrum.output import open_loggs
from spectrum.tools.feeddown import data_feeddown
from vault.datavault import DataVault


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


class YieldExtractioinUncertanityOptions(object):
    def __init__(self, cyield):
        self.mass_range = {
            "low": [0.06, 0.22],
            "mid": [0.04, 0.20],
            "wide": [0.08, 0.24]
        }
        self.backgrounds = ["pol2", "pol1"]
        self.signals = ["CrystalBall", "Gaus"]
        self.nsigmas = [2]
        self.cyield = cyield


class YieldExtractioin(TransformerBase):

    def __init__(self, options, plot=False):
        super(YieldExtractioin, self).__init__(plot)
        self.options = options
        self.plot = plot

    def transform(self, data, loggs):
        spectrums = []
        pbar = tqdm.tqdm(
            total=len(self.options.mass_range) *
            len(self.options.backgrounds) *
            len(self.options.signals) *
            len(self.options.nsigmas)
        )
        for flab, frange in six.iteritems(self.options.mass_range):
            for bckgr in self.options.backgrounds:
                for marker, par in enumerate(self.options.signals):
                    for nsigmas in self.options.nsigmas:
                        msg = "n#sigma = {} {} {} {}"
                        label = msg.format(nsigmas, par, bckgr, flab)

                        options = Options()
                        options.calibration.dead = True
                        options.calibration.nsigmas = nsigmas
                        options.invmass.signal.fitf = par
                        options.invmass.signal.background = bckgr
                        options.invmass.signal.fit_range = frange

                        self.options.cyield.analysis = options
                        with open_loggs() as loggs_local:
                            estimator = CorrectedYield(self.options.cyield)
                            spectrum = estimator.transform(data, loggs_local)
                            # loggs.update({label: loggs_local})
                        spectrum.marker = marker
                        spectrum.label = label
                        spectrums.append(spectrum)
                        pbar.update()
        pbar.close()
        diff = Comparator(stop=self.plot, oname="spectrum_extraction_methods")
        diff.compare(spectrums, loggs=loggs)

        average = br.average(spectrums, "averaged yield")
        diff = Comparator(stop=True, oname="yield_deviation_from_average")
        diff.compare_ratios(spectrums, average, loggs=loggs)

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
