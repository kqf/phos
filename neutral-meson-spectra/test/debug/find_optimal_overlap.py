import unittest
from collections import OrderedDict

import ROOT
from spectrum.broot import BROOT as br
from spectrum.comparator import Comparator
from spectrum.efficiency import Efficiency
from spectrum.options import CompositeEfficiencyOptions
from spectrum.output import AnalysisOutput
from spectrum.pipeline import ParallelPipeline, Pipeline
from spectrum.transformer import TransformerBase
from tools.scan import NonlinearityParamExtractor, form_histnames
from vault.datavault import DataVault


class OverlapParamExtractor(NonlinearityParamExtractor):

    def read_labels(self, data):
        output = []
        for d in data:
            high, low = d
            real, mixing = low.transform()
            output.append(
                map(float, real.GetTitle().split())
            )
        return output


class OverlapNonlinearityScan(TransformerBase):
    def __init__(self, options, nbins, chi2_=br.chi2ndf, plot=True):
        super(OverlapNonlinearityScan, self).__init__()
        chi2 = ParallelPipeline([
            ("efficiency" + str(i), Efficiency(options))
            for i in range(nbins ** 2)
        ])

        extractor = OverlapParamExtractor()
        self.pipeline = Pipeline([
            ("read-titles", extractor),
            ("chi2", chi2),
            ("dump", extractor)
        ])


def add_arguments(identity, original):
    identity.filename = original.filename
    identity.histname = original.histname
    identity.listname = original.listname
    identity.events = original.events
    identity.label = original.label
    return identity


# TODO: Add Calculate only inside the overlap region
# TODO: Remove unnecessary configuration from the options effname
class ScanNonlinearitiesOverlap(unittest.TestCase):

    def test(self):
        nbins = 2
        prod = "single #pi^{0} scan nonlinearity"
        histnames = form_histnames(nbins)
        low = DataVault().input(prod, "low", inputs=histnames)
        high = DataVault().input(prod, "high", inputs=histnames)

        unified_inputs = OrderedDict([
            (low, (0.0, 8.0)),
            (high, (4.0, 20.0)),
        ])
        options = CompositeEfficiencyOptions(unified_inputs, "#pi^{0}",
                                             selname="PhysEff")
        options.reduce_function = lambda x: br.chi2ndf(*x)

        low_, high_ = low.read_multiple(2), high.read_multiple(2)
        low_ = [add_arguments(l, low) for l in low_]
        high_ = [add_arguments(l, high) for l in high_]
        mc_data = [(l, h) for l, h in zip(low_, high_)]

        chi2ndf = OverlapNonlinearityScan(options, nbins).transform(
            mc_data,
            loggs=AnalysisOutput("testing the scan interface")
        )
        Comparator().compare(chi2ndf)
