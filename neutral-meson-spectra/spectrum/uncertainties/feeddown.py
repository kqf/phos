import numpy as np
import array
import ROOT

from spectrum.options import Options
from spectrum.pipeline import TransformerBase
import spectrum.broot as br
from spectrum.tools.kaon2pion import K2POptions
from spectrum.tools.kaon2pion import KaonToPionRatioData
from vault.datavault import DataVault


def feeddown_data():
    return (
        DataVault().input("kaon2pion"),
        DataVault().input("kaon2pion"),
    )


class FeedDownOptions(object):

    def __init__(self, particle="#pi^{0}"):
        super(FeedDownOptions, self).__init__()
        if particle != "#pi^{0}":
            raise IOError("Feeddown for {} is not defined".format(particle))
        self.edges = Options(particle).pt.ptedges
        self.title = "; p_{T}, GeV/c ;relative sys. uncertainty"
        # The value borrowed from the 5 TeV analysis
        self.uncertainty_value = 0.02
        self.k2p = K2POptions(
            kaons="hsys_kaon_pp13_sum",
            pions="hsys_pion_pp13_sum"
        )


class FeedDown(TransformerBase):
    def __init__(self, options, plot=False):
        self.options = options
        self.pipeline = KaonToPionRatioData(self.options.k2p)

    def transform(self, data, loggs):
        k2p = self.pipeline.transform(data, loggs)
        bins = br.bins(k2p)
        relative_uncertainties = bins.errors / bins.contents
        relative_uncertainties[np.isnan(relative_uncertainties)] = 0
        uncertainty_value = max(relative_uncertainties)

        edges = array.array('d', self.options.edges)
        uncertainty = ROOT.TH1F("feeddown",
                                self.options.title,
                                len(edges) - 1,
                                edges)

        for i in br.hrange(uncertainty):
            uncertainty.SetBinContent(i, uncertainty_value)
        uncertainty.label = "feed-down uncertainty"
        uncertainty.Scale(0.1)
        return uncertainty
