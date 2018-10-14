import unittest
from vault.datavault import DataVault


class TestDatasets(unittest.TestCase):

    def test_input_data_is_valid(self):
        self.check_ledger("ledger.json")

    def test_debug_data_is_valid(self):
        self.check_ledger("debug-ledger.json")

    def check_ledger(self, ledger):
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
        self.assertTrue(len(bad_datasets) == 0, msg=message)
