import numpy as np
import array
import ROOT

from spectrum.options import Options
from spectrum.pipeline import TransformerBase
import spectrum.broot as br
from spectrum.tools.kaon2pion import KaonToPionRatioData
from spectrum.vault import DataVault


def feeddown_data():
    return (
        DataVault().input("kaon2pion", histname="hstat_kaon_pp13_sum"),
        DataVault().input("kaon2pion", histname="hstat_pion_pp13_sum"),
    )


class FeedDownOptions(object):

    def __init__(self, particle="#pi^{0}"):
        super(FeedDownOptions, self).__init__()
        if particle != "#pi^{0}":
            raise IOError("Feeddown for {} is not defined".format(particle))
        self.edges = Options(particle).pt.ptedges
        self.title = "; p_{T} (GeV/#it{c}) ;relative sys. uncertainty"
        # The value borrowed from the 5 TeV analysis
        self.uncertainty_value = 0.02


class FeedDown(TransformerBase):
    def __init__(self, options, plot=False):
        self.pipeline = KaonToPionRatioData()
        self.options = options

    def transform(self, data, loggs):
        k2p = self.pipeline.transform(data, loggs)
        bins = br.bins(k2p)
        relative_uncertainties = bins.errors / bins.contents
        relative_uncertainties[np.isnan(relative_uncertainties)] = 0
        print(relative_uncertainties)
        uncertainty_value = max(relative_uncertainties)

        edges = array.array('d', self.options.edges)
        uncertainty = ROOT.TH1F("feeddown",
                                self.options.title,
                                len(edges) - 1,
                                edges)

        for i in br.hrange(uncertainty):
            uncertainty.SetBinContent(i, uncertainty_value)
            uncertainty.SetBinError(i, 0)
        uncertainty.label = "feed-down uncertainty"
        uncertainty.Scale(0.1)
        return uncertainty
