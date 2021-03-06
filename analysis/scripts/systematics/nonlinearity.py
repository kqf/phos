import pytest

import joblib
import numpy as np
import spectrum.broot as br
import spectrum.plotter as plt
from spectrum.output import open_loggs
from spectrum.comparator import Comparator

from spectrum.uncertainties.nonlinearity import NonlinearityUncertainty
from spectrum.uncertainties.nonlinearity import NonlinearityUncertaintyOptions
from spectrum.uncertainties.nonlinearity import nonlinearity_scan_data
from spectrum.pipeline import ParallelPipeline
from spectrum.efficiency import Efficiency

from spectrum.options import CompositeEfficiencyOptions
from spectrum.pipeline import ComparePipeline
from spectrum.vault import DataVault


@pytest.fixture
def nbins():
    return 9


memory = joblib.Memory(".joblib-cachedir", verbose=0)


@memory.cache()
def nonlin_tests(particle, nbins, stop):
    prod = "single #pi^{0} nonlinearity scan"
    options = NonlinearityUncertaintyOptions(particle=particle, nbins=nbins)

    with open_loggs() as loggs:
        uncert = NonlinearityUncertainty(options, plot=stop).transform(
            nonlinearity_scan_data(nbins, prod),
            loggs
        )

    return uncert

# Benchmark:
# In the 5 TeV analysis U_nonlin ~ 0.01


@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    # "#eta",
])
def test_nonlinearity_uncertainty(particle, nbins, stop):
    uncert = nonlin_tests(particle, nbins, stop)
    nonlin = br.bins(uncert)

    Comparator(stop=stop).compare(uncert)

    print()
    maxerror = np.max(nonlin.contents)
    print("\\def \\nonlinearityMaxError {{{}}}".format(maxerror))

    maxpT = nonlin.centers[np.argmax(nonlin.contents)]
    print("\\def \\nonlinearityMaxErrorPt {{{}}}".format(maxpT))

    average = nonlin.contents.mean()
    print("\\def \\nonlinearityAverageError {{{}}}".format(average))


@pytest.fixture
def spmc_data():
    return (
        DataVault().input("single #pi^{0}", "low", "PhysEff"),
        DataVault().input("single #pi^{0}", "high", "PhysEff"),
    )


@pytest.fixture
def scan_data():
    prod = "single #pi^{0} nonlinearity scan"
    return (
        DataVault().input(prod, "low", "PhysEff"),
        DataVault().input(prod, "high", "PhysEff"),
    )


@pytest.mark.skip("This one is used only to check the uncertainties by eyes")
@pytest.mark.onlylocal
@pytest.mark.interactive
def test_spmc_efficiency(spmc_data, scan_data):
    options = CompositeEfficiencyOptions("#pi^{0}")
    estimator = ComparePipeline([
        ("spmc", Efficiency(options)),
        ("scan", Efficiency(options)),
    ], plot=True)
    with open_loggs("test") as loggs:
        estimator.transform((spmc_data, scan_data), loggs)


@pytest.mark.skip
@pytest.mark.onlylocal
@pytest.mark.interactive
def test_problematic_productions(nbins):
    prod = "single #pi^{0} nonlinearity scan"
    data = nonlinearity_scan_data(nbins, prod)[:3]
    options = NonlinearityUncertaintyOptions()
    mc = ParallelPipeline([
        ("efficiency_" + str(i), Efficiency(options.eff))
        for i, _ in enumerate(data)
    ], disable=False)

    with open_loggs() as loggs:
        output = mc.transform(data, loggs)
    Comparator().compare(output)
