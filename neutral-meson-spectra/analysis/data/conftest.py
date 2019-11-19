import pytest
from vault.datavault import DataVault


@pytest.fixture
def data():
    return DataVault().input("data", histname="MassPtSM0")
