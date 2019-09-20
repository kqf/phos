from joblib import Memory

from spectrum.output import open_loggs
from spectrum.pipeline import Pipeline
from spectrum.pipeline import ParallelPipeline
from spectrum.pipeline import FunctionTransformer
from spectrum.pipeline import TransformerBase

from spectrum.uncertainties.acceptance import Acceptance
from spectrum.uncertainties.acceptance import AcceptanceOptions
from spectrum.uncertainties.acceptance import acceptance_data

from spectrum.uncertainties.tof import TofUncertainty
from spectrum.uncertainties.tof import TofUncertaintyOptions
from spectrum.uncertainties.tof import tof_data

from spectrum.uncertainties.gscale import GScale
from spectrum.uncertainties.gscale import GScaleOptions
from spectrum.uncertainties.gscale import ge_scale_data

from spectrum.uncertainties.nonlinearity import NonlinearityUncertainty
from spectrum.uncertainties.nonlinearity import NonlinearityUncertaintyOptions
from spectrum.uncertainties.nonlinearity import nonlinearity_scan_data

from spectrum.uncertainties.yields import YieldExtractioin
from spectrum.uncertainties.yields import YieldExtractioinUncertanityOptions
from spectrum.uncertainties.yields import yield_extraction_data


from spectrum.uncertainties.feeddown import FeedDown
from spectrum.uncertainties.feeddown import FeedDownOptions
from spectrum.uncertainties.feeddown import feeddown_data

from spectrum.uncertainties.material import MaterialBudget
from spectrum.uncertainties.material import MaterialBudgetOptions
from spectrum.uncertainties.material import material_budget_data


NBINS = 5


def data():
    return (
        yield_extraction_data(),
        nonlinearity_scan_data(NBINS, "single #pi^{0}"),
        tof_data(),
        ge_scale_data("#pi^{0}"),
        acceptance_data(),
        feeddown_data(),
        material_budget_data(),
    )


memory = Memory(".joblib-cachedir", verbose=0)


@memory.cache()
def uncertainties(particle, data):
    options = TotalUncertaintyOptions(particle=particle)
    estimator = ParallelPipeline([
        ("yield", YieldExtractioin(options.yields)),
        ("nonlinearity", NonlinearityUncertainty(options.nonlin)),
        ("tof", TofUncertainty(options.tof)),
        ("gescale", GScale(options.gescale)),
        ("accepntace", Acceptance(options.acceptance)),
        ("feed down", FeedDown(options.feeddown)),
        ("material budget", MaterialBudget(options.material))
    ])
    with open_loggs() as loggs:
        output = estimator.transform(data, loggs)
    print("Systematics is done")
    return output


class TotalUncertaintyOptions():
    def __init__(self, particle):
        self.yields = YieldExtractioinUncertanityOptions(particle=particle)
        self.nonlin = NonlinearityUncertaintyOptions(nbins=NBINS)
        self.tof = TofUncertaintyOptions()
        self.gescale = GScaleOptions(particle=particle)
        self.acceptance = AcceptanceOptions(particle=particle)
        self.feeddown = FeedDownOptions(particle=particle)
        self.material = MaterialBudgetOptions(particle=particle)
        self.particle = particle


class TotalUncertainty(TransformerBase):
    def __init__(self, options, plot=False):
        particle = options.particle
        self.pipeline = Pipeline([
            ("efficiencies", FunctionTransformer(
                lambda data, loggs: uncertainties(particle, data)
            )),
            ("sum", self.sum)
        ])

    def sum(self, data, loggs):
        return None
