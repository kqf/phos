import pytest

from vault.datavault import DataVault


@pytest.mark.onlylocal
def test_input_data_is_valid():
    check_ledger("ledger.json")


@pytest.mark.onlylocal
def test_debug_data_is_valid():
    check_ledger("debug-ledger.json")


def check_ledger(ledger):
    bad_datasets = DataVault(ledger).validate_all_datasets()
    ill_datasets = "\n".join(
        ["{0} {1}. Wrong hash, the actual one: {2}".format(*d)
         for d in bad_datasets]
    )
    message = "\n\nIn the ledger {}\n".format(ledger)
    message += "Your don't have enough data. " + \
        "Some files are changed or missing\n\n{0}".format(
            ill_datasets)
    # NB: test dataset is always missing
    assert len(bad_datasets) == 0, message
