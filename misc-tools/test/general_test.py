#!/usr/bin/python


import unittest
import os

from drawtools.style import Styler


# Use multiple inheritance to avoid 
# problem of calling tests from parent classes
#

class GeneralTest(object):
	def __init__(self):
		super(GeneralTest, self).__init__()
		self.conffile = None

	def testDrawing(self):
		style = Styler(self.conffile)
		style.draw()

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



		
