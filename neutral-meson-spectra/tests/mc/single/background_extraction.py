import random
import pytest  # noqa

import spectrum.sutils as su
from spectrum.broot import BROOT as br  # noqa
from spectrum.comparator import Comparator  # noqa
from spectrum.input import Input
from spectrum.options import Options
from spectrum.output import AnalysisOutput
from spectrum.parametrisation import PeakParametrisation
from spectrum.pipeline import Pipeline
from spectrum.processing import DataSlicer, MassFitter
from spectrum.ptplotter import MassesPlot
from spectrum.output import open_loggs
from vault.datavault import DataVault


class BackgroundTransformer:
    def transform(self, masses, loggs):
        for mass in masses:
            map(
                mass.mass.Fill,
                [random.uniform(0.08, 0.2) for i in range(50)],
                [mass.pt_range[0] + (mass.pt_range[1] -
                                     mass.pt_range[0]) / 2. for i in range(50)]
            )
        return masses


class MassExtractor(object):

    def __init__(self, options=Options()):
        super(MassExtractor, self).__init__()
        self.options = options
        self._loggs = None

    def transform(self, inputs, loggs):
        pipeline = Pipeline([
            ("slice", DataSlicer(self.options.pt)),
            ("background", BackgroundTransformer()),
            ("fitmasses", MassFitter(self.options.invmass)),
        ])

        output = pipeline.transform(inputs, loggs)
        return output


@pytest.mark.skip("")
def test_background_fitting():
    loggs = AnalysisOutput("test_spmc_background", "#pi^{0}")

    with open_loggs("test spmc background") as loggs:
        options = Options.spmc((4.0, 20.0))
        # options.fitf = 'gaus'
        masses = MassExtractor(options).transform(
            # Input(DataVault().file("single #pi^{0}", "high"), "PhysEff"),
            Input("LHC16-single.root", "PhysEff"),
            loggs
        )

    target = masses[8]
    param = PeakParametrisation.get(options.invmass.backgroundp)
    fitf, background = param.fit(target.mass)

    canvas = su.canvas("test")
    MassesPlot().transform(target, canvas)
    # target.mass.GetXaxis().SetRangeUser(*target.initial_fitting_region)
    # target.mass.Draw()
    # fitf.Draw("same")
    canvas.Update()
    su.wait()

    # signal = ROOT.TF1(
    #     "pure_peak",
    #     lambda x, p: fitf.Eval(x[0]) - background.Eval(x[0]), 0, 1, 10)
    # parameters = [fitf.GetParameter(i) for i in range(fitf.GetNpar())]
    # signal.SetParameters(*parameters)
    # for i in range(fitf.GetNpar()):
    #     signal.SetParameter(i, fitf.GetParameter(i))

    # print signal.GetParameter(0), fitf.GetParameter(0)

    # target.mass.Add(signal, -1)
    # residualb = ROOT.TF1("residual", "pol2(0)", 0.1, 0.16)
    # target.mass.Fit(residualb)
    # diff = Comparator()

    # diff.compare(
    #     br.rebin_as(target.mass, background.GetHistogram())
    # )


def test_data_peak():
    with open_loggs("test_spmc_background") as loggs:
        options = Options()
        # options.fitf = 'gaus'
        masses = MassExtractor(options).transform(
            DataVault().input("data"),
            loggs
        )

    target = masses[12]
    param = PeakParametrisation.get(options.invmass.backgroundp)
    fitf, background = param.fit(target.mass)

    canvas = su.canvas("test")
    MassesPlot().transform(target, canvas)
    # target.mass.GetXaxis().SetRangeUser(*target.initial_fitting_region)
    # target.mass.Draw()
    # fitf.Draw("same")
    canvas.Update()
    su.wait()
