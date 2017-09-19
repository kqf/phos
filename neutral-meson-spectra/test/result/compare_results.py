import os
import json
import unittest

from spectrum.broot import BROOT as br
from spectrum.comparator import Comparator



def download_data(directory = 'input-data/'):
    with open('config/links.json') as f:
        conf = json.load(f)

    for fname, record in conf.iteritems():
    	infile = directory + fname
    	if os.path.isfile(infile):
    		continue
    	br.io.hepdata(record, infile)

    return conf.keys()



class ComparePublishedResults(unittest.TestCase):
	infiles = download_data()

	def setUp(self):
		tdir = 'Table 1'
		hname = 'Hist1D_y1'
		self.hreader = lambda h: br.io.read(h, tdir, hname)

	def test(self):
		histograms = map(self.hreader, self.infiles)

		for name, hist in zip(self.infiles, histograms):
			label = name.replace('.', ' ')
			label = name.replace('root', '')
			hist.label = label
			hist.logy = 1
			hist.logx = 1
			hist.GetYaxis().SetTitleOffset(1.2)
			hist.Scale(1. / 10 ** (2* int(label[0])))

		diff = Comparator()
		diff.compare(histograms)

