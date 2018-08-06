import ROOT
import tqdm
from spectrum.broot import BROOT as br
from spectrum.comparator import Comparator
from spectrum.corrected_yield import CorrectedYield
from spectrum.options import Options
from spectrum.transformer import TransformerBase


class YieldExtractioin(TransformerBase):

    def __init__(self, options, plot=False):
        super(YieldExtractioin, self).__init__(plot)
        self.options = options
        self.plot = plot

    def average_yiled(self, histos):
        average = histos[0].Clone(histos[0].GetName() + "_average")
        average.Reset()
        average.Sumw2()
        llist = ROOT.TList()

        for h in histos:
            llist.Add(h)

        average.Merge(llist)
        average.Scale(1. / len(histos))
        average.label = "averaged yield"
        return average

    def transform(self, data, loggs):
        spectrums = []
        pbar = tqdm.tqdm(
            total=len(self.options.mass_range) *
            len(self.options.backgrounds) *
            len(self.options.signals) *
            len(self.options.nsigmas)
        )
        for frange, flab in self.options.mass_range.iteritems():
            for bckgr in self.options.backgrounds:
                for marker, par in enumerate(self.options.signals):
                    for nsigmas in self.options.nsigmas:
                        options = Options()
                        options.spectrum.dead = True
                        options.pt.label = "n#sigma = {0} {1} {2} {3}".format(
                            nsigmas, par, bckgr, flab)
                        options.spectrum.nsigmas = nsigmas
                        options.signalp.fitf = par
                        options.signalp.background = bckgr
                        options.signalp.fit_range = frange

                        self.options.analysis = options
                        spectrum = CorrectedYield(
                            self.options.cyield).transform(data, loggs)
                        spectrum.marker = marker
                        spectrums.append(spectrum)
                        pbar.update()
        pbar.close()
        diff = Comparator(stop=self.plot, oname="spectrum_extraction_methods")
        diff.compare(spectrums)

        average = self.average_yiled(spectrums)
        diff = Comparator(stop=self.plot, oname="yield_deviation_from_average")
        diff.compare_ratios(spectrums, average)

        uncert, rms, mean = br.systematic_deviation(spectrums)
        uncert.SetTitle(
            "Systematic uncertanity from yield extraction (RMS/mean)")
        diff = Comparator(stop=self.plot, oname="syst-error-yield-extraction")
        diff.compare(uncert)
        return uncert
