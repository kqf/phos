import unittest
from vault.datavault import DataVault


class TestDatasets(unittest.TestCase):

	def test_input_data_is_valid(self):
		bad_datasets = DataVault().validate_all_datasets()
		ill_datasets = "\n".join(["{0} {1}. Wrong hash or missing file {2}".format(*d) for d in bad_datasets])
		message = "Your don't have enough data. Some files are changed or missing\n\n{0}".format(ill_datasets)
		# NB: test dataset is always missing
		self.assertTrue(len(bad_datasets) == 1, msg=message)
