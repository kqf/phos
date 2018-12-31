import pytest

from lazy_object_proxy import Proxy
from spectrum.efficiency import Efficiency
from spectrum.comparator import Comparator
from vault.datavault import DataVault
from spectrum.output import AnalysisOutput
from spectrum.options import EfficiencyOptions

DATA_ETA = Proxy(
    lambda: DataVault().input("single #eta", "high", "PhysEff")
)
DATA_PION = Proxy(
    lambda: DataVault().input("single #pi^{0}", "high", "PhysEff")
)


@pytest.mark.onlylocal
@pytest.mark.parametrize("particle, data", [
    ("#pi^{0}", DATA_ETA),
    ("#eta", DATA_PION),
])
def test_high_momentum(particle, data):
    options = EfficiencyOptions()
    edges = [
        6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0, 10.5, 11.0, 11.5,
        12.0, 12.5, 13.0, 13.5, 14.0, 14.5, 15.0, 15.5, 16.0, 16.5, 17.0,
        17.5, 18.0, 18.5, 19.0, 19.5, 20.0
    ]
    rebins = [0] * (len(edges) - 1)
    options.analysis.pt.ptedges = edges
    options.analysis.pt.rebins = rebins
    options.analysis.invmass.use_mixed = False

    loggs = AnalysisOutput("test high momentum {}".format(particle))
    efficiency = Efficiency(options).transform(data, loggs)
    efficiency.SetTitle('Efficiency at high p_{T}')

    diff = Comparator()
    diff.compare(efficiency)
    loggs.plot(False)
