import os
import unittest
from vault.datavault import DataVault

class TestVault(unittest.TestCase):


	def setUp(self):
		self.filename = 'input-data/test_vault.root'
		with open(self.filename, 'wb') as f:
			f.write("This is a test file for DataVault")


	def tearDown(self):
		os.remove(self.filename)


	def test_reads_filename(self):
		vault = DataVault()

		self.assertEqual(vault.file("test"), self.filename)
