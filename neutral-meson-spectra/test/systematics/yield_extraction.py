from spectrum.options import Options
from spectrum.comparator import Comparator

from spectrum.broot import BROOT as br
from systematic_error import SysError
from spectrum.efficiency import Efficiency
from spectrum.corrected_yield import CorrectedYield
from spectrum.options import CorrectedYieldOptions

import ROOT


class RawYieldError(object):

    def __init__(self, stop):
        super(RawYieldError, self).__init__()
        # This should be studied on corrected yield
        #
        self.infile = 'LHC16'
        self.selection = 'PhysOnlyTender'
        self.outsys = SysError(label='yield extraction')
        self.stop = stop

        # Calculate efficiency to correct the yield
        #
        effile = 'Pythia-LHC16-a5'
        effhist = 'hPt_#pi^{0}_primary_'
        self.eff = Efficiency(effhist, 'eff', effile).eff()

    def average_yiled(self, histos):
        average = histos[0].Clone(histos[0].GetName() + '_average')
        average.Reset()
        average.Sumw2()
        llist = ROOT.TList()

        for h in histos:
            llist.Add(h)

        average.Merge(llist)
        average.Scale(1. / len(histos))
        average.label = 'averaged yield'
        return average

    def transofrm(self, data, loggs):
        spectrums, options = [], Options()
        for frange, flab in zip([[0.06, 0.22], [0.04, 0.20], [0.08, 0.24]], ['low', 'mid', 'wide']):
            for bckgr in ['pol1', 'pol2']:
                for marker, par in enumerate(['CrystalBall', 'Gaus']):
                    for nsigmas in [2, 3]:
                        options.spectrum.dead = True
                        options.pt.label = 'n#sigma = {0} {1} {2} {3}'.format(
                            nsigmas, par, bckgr, flab)
                        options.spectrum.nsigmas = nsigmas
                        options.param.fitf = par
                        options.param.background = bckgr
                        options.param.fit_range = frange

                        copt = CorrectedYieldOptions()
                        copt.analysis = options
                        spectrum = CorrectedYield(copt).transform(data, loggs)
                        spectrum.marker = marker
                        spectrums.append(spectrum)

        diff = Comparator(stop=self.stop, oname='spectrum_extraction_methods')
        diff.compare(spectrums)

        average = self.average_yiled(spectrums)
        diff = Comparator(stop=self.stop, oname='yield_deviation_from_average')
        diff.compare_ratios(spectrums, average)

        uncert, rms, mean = br.systematic_deviation(spectrums)
        uncert.SetTitle(
            'Systematic uncertanity from yield extraction (RMS/mean)')
        diff = Comparator(stop=self.stop, oname='syst-error-yield-extraction')
        diff.compare(uncert)
        return self.outsys.histogram(spectrums[0], uncert)
