#!/usr/bin/python

import ROOT
import os

class Averager(object):
	def __init__(self, path):
		super(Averager, self).__init__()
		self.path = path
		
	def get_files(self):
		return os.listdir(self.path)

	def average(self, predicate):
		average = None
		good_files = (f for f in self.get_files() if '.root' in f and predicate(int(f.split('.')[0])))
		i = 0
		for f in good_files:
			hist = ROOT.TFile.Open(self.path + '/' + f).HeatMaps.FindObject('hHeatMapInSM3')
			i = i + 1

			if not average: 
				average = hist.Clone('haverage')
				continue

			average.Add(hist)
		average.Scale(1. / average.Integral())
		print i
		return average
		

def main():
	av = Averager('LHC16k')

	bad_run =  lambda x: x >= 256944 and x <= 257145
	good_run = lambda x: (not bad_run(x)) and x < 258399 

	heatmap_good = av.average(good_run)
	heatmap_bad  = av.average(bad_run)

	canvas = ROOT.TCanvas('c1', 'Test', 900, 500)
	canvas.Divide(3, 1)
	canvas.cd(1)
	heatmap_good.SetTitle('Good runs')
	heatmap_good.Draw('colz')
	
	canvas.cd(2)
	heatmap_bad.SetTitle('Bad runs')
	heatmap_bad.Draw('colz')

	canvas.cd(3)
	diff = heatmap_bad.Clone('diff')
	diff.Add(heatmap_good, -1)
	diff.SetTitle('BadRuns - GoodRuns')
	diff.Draw('colz')
	canvas.Update()

	raw_input('Press any key ...')


if __name__ == '__main__':
	main()