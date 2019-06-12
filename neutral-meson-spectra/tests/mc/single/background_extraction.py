import random
import pytest  # noqa

import spectrum.sutils as su
from spectrum.broot import BROOT as br  # noqa
from spectrum.comparator import Comparator  # noqa
from spectrum.input import Input
from spectrum.options import Options
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


@pytest.fixture
def single_input():
    return Input("LHC16-single.root", "PhysEff")


@pytest.mark.skip("")
def test_background_fitting(single_input):
    with open_loggs("test spmc background") as loggs:
        options = Options()
        # options.fitf = 'gaus'
        masses = MassExtractor(options).transform(single_input, loggs)

    target = masses[8]
    param = PeakParametrisation.get(options.invmass.backgroundp)
    fitf, background = param.fit(target.mass)

    canvas = su.canvas("test")
    MassesPlot().transform(target, canvas)
    canvas.Update()
    su.wait()


@pytest.fixture
def data():
    return DataVault().input("data")


@pytest.mark.onlylocal
@pytest.mark.onlylocal
def test_data_peak(data):
    with open_loggs("test spmc background") as loggs:
        options = Options()
        masses = MassExtractor(options).transform(data, loggs)

    target = masses[12]
    param = PeakParametrisation.get(options.invmass.backgroundp)
    fitf, background = param.fit(target.mass)

    canvas = su.canvas("test")
    MassesPlot().transform(target, canvas)
    canvas.Update()
    su.wait()
