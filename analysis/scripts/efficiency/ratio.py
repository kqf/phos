import pytest

from spectrum.pipeline import ComparePipeline
from spectrum.efficiency import Efficiency, efficiency_data
from spectrum.options import CompositeEfficiencyOptions
from spectrum.output import open_loggs


@pytest.fixture
def ratio_data():
    return efficiency_data("#eta"), efficiency_data("#pi^{0}")


@pytest.mark.interactive
@pytest.mark.onlylocal
def test_efficiency_ratio(ratio_data):
    pt = "config/pt-same.json"
    estimator = ComparePipeline([
        ("#eta", Efficiency(CompositeEfficiencyOptions("#eta", pt=pt))),
        ("#pi^{0}", Efficiency(CompositeEfficiencyOptions("#pi^{0}", pt=pt))),
    ])
    with open_loggs() as loggs:
        estimator.transform(ratio_data, loggs)
