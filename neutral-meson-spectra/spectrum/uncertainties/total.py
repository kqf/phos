import ROOT
import numpy as np
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
from spectrum.uncertainties.gscale import gscale_data

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

from spectrum.plotter import hplot
import spectrum.broot as br


NBINS = 9


def data_total_uncert(particle):
    data = [
        yield_extraction_data(particle=particle),
        nonlinearity_scan_data(NBINS, "single #pi^{0} nonlinearity scan"),
        tof_data(),
        gscale_data(particle),
        acceptance_data(),
        material_budget_data(),
    ]

    if particle == "#pi^{0}":
        data.append(feeddown_data())
    return data


memory = Memory(".joblib-cachedir", verbose=0)


@memory.cache()
def errors(data, particle):
    options = TotalUncertaintyOptions(particle=particle)
    steps = [
        ("yield extraction", YieldExtractioin(options.yields)),
        ("nonlinearity", NonlinearityUncertainty(options.nonlin)),
        ("tof", TofUncertainty(options.tof)),
        ("global energy scale", GScale(options.gescale)),
        ("acceptance", Acceptance(options.acceptance)),
        ("material budget", MaterialBudget(options.material))
    ]

    if particle == "#pi^{0}":
        steps.append(("feed down", FeedDown(options.feeddown)))

    estimator = ParallelPipeline(steps)

    with open_loggs() as loggs:
        output = estimator.transform(data, loggs)

    labels, _ = zip(*steps)
    for hist, label in zip(output, labels):
        hist.SetTitle(label)
        hist.GetYaxis().SetTitle("rel. sys. error")
        hist.SetLineColor(-1)
        hist.SetAxisRange(0, 1, "Y")
        for i in br.hrange(hist):
            hist.SetBinError(i, 0)

    return output


class TotalUncertaintyOptions():
    title = "Total systematic uncertainty; " \
        "p_{T} (GeV/#it{c}), relative sys. err."

    def __init__(self, particle):
        self.yields = YieldExtractioinUncertanityOptions(particle=particle)
        self.nonlin = NonlinearityUncertaintyOptions(
            particle=particle, nbins=NBINS)
        self.tof = TofUncertaintyOptions(particle=particle)
        self.gescale = GScaleOptions(particle=particle)
        self.acceptance = AcceptanceOptions(particle=particle)
        self.material = MaterialBudgetOptions(particle=particle)
        self.particle = particle
        if particle == "#pi^{0}":
            self.feeddown = FeedDownOptions(particle=particle)

        self.steps = [
            "yield extraction",
            "nonlinearity",
            "tof",
            "global energy scale",
            "acceptance",
            "material budget",
        ]
        if particle == "#pi^{0}":
            self.steps.append("feed down")


class TotalUncertainty(TransformerBase):
    def __init__(self, options, plot=False):
        particle = options.particle
        self.options = options
        self.pipeline = Pipeline([
            ("errors", FunctionTransformer(errors, True, particle=particle)),
            ("sum", FunctionTransformer(self.sum))
        ])
        self.steps = options.steps

    def sum(self, data, loggs):
        uncertainties = np.array([br.bins(h).contents for h in data])
        total_uncert = (uncertainties ** 2).sum(axis=0) ** 0.5
        total_hist = data[0].Clone("total_uncertainty")
        total_hist.SetTitle("total")
        # The total histogram should be black
        total_hist.SetLineColor(ROOT.kBlack)
        for i in br.hrange(total_hist):
            total_hist.SetBinContent(i, total_uncert[i - 1])

        hplot(
            list(data) + [total_hist],
            logx=False,
            logy=False,
            xtitle="p_{T} (GeV/#it{c})",
            csize=(96, 128),
            legend_pos=(0.2, 0.7, 0.4, 0.85),
            oname="results/systematics/total/{}.pdf".format(
                br.spell(self.options.particle)
            ),
            more_logs=False,
            yoffset=1.6,
            # ltitle="{} #rightarrow #gamma #gamma".format(
            #     self.options.particle
            # ),
        )
        return total_hist
