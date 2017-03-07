#!/usr/bin/python


import unittest
import os

class TestImages(unittest.TestCase):

	def setUp(self):
		# Different values in some pt-bins can be explained by limited statistics in those bins.
		#
		# This one should be changed later
		self.conffile, self.infile, histname = self.save_config()
		self.save_histogram(self.infile, histname)

	def save_config(self):
		pass

	def save_histogram(self):
		pass


	def tearDown(self):
		os.remove(self.conffile)
		os.remove(self.infile)


