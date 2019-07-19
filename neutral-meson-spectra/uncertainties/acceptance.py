from spectrum.pipeline import TransformerBase
from spectrum.options import CompositeCorrectedYieldOptions
from spectrum.pipeline import ReduceArgumentPipeline
from spectrum.pipeline import ParallelPipeline
from spectrum.pipeline import Pipeline
from spectrum.corrected_yield import CorrectedYield
from spectrum.broot import BROOT as br
from spectrum.comparator import Comparator
from tools.unityfit import UnityFitTransformer
from tools.feeddown import data_feeddown
from vault.datavault import DataVault


def cyield_data(particle, cut):
    mc_production = "single {}".format(particle)
    data_input = (
        DataVault().input(
            "data", "latest",
            listname="Phys{}".format(cut),
            histname="MassPtSM0"),
        data_feeddown(),
    )
    mc_inputs = (
        DataVault().input(
            mc_production, "low",
            listname="PhysEff{}".format(cut),
            # histname="MassPtSM0"
        ),
        DataVault().input(
            mc_production, "high",
            listname="PhysEff{}".format(cut),
            # histname="MassPtSM0"
        ),
    )
    return data_input, mc_inputs


def acceptance_data(particle="#pi^{0}"):
    return (
        cyield_data(particle, cut=0),
        (
            cyield_data(particle, cut=1),
            cyield_data(particle, cut=2),
            cyield_data(particle, cut=3),
        ),
    )


class AcceptanceOptions(object):
    title = "Acceptance uncertainty; p_{T}, GeV/c; Relateive error, %"

    def __init__(self, particle="#pi^{0}"):
        super(AcceptanceOptions, self).__init__()
        self.cyield = CompositeCorrectedYieldOptions(particle)
        self.fit_range = (1, 10)


class MaxUnityHistogram(object):
    def transform(self, hists, loggs):
        return max(hists, key=lambda x: x.GetBinContent(1))


class SaveImagesTransformer(object):
    def transform(self, hists, loggs):
        Comparator().compare(hists, loggs=loggs)
        return hists


class Acceptance(TransformerBase):
    def __init__(self, options, plot=False):
        super(Acceptance, self).__init__(plot)
        unities = ReduceArgumentPipeline(
            ParallelPipeline([
                ("dist 1", CorrectedYield(options.cyield)),
                ("dist 2", CorrectedYield(options.cyield)),
                ("dist 3", CorrectedYield(options.cyield)),
            ]),
            CorrectedYield(options.cyield),
            br.ratio
        )

        self.pipeline = Pipeline([
            ("unities", unities),
            ("images", SaveImagesTransformer()),
            ("fit", UnityFitTransformer(options.title, options.fit_range)),
            ("max", MaxUnityHistogram()),
        ])
