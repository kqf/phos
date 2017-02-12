#!/usr/bin/python

import ROOT

		# tpc.Draw()
		# canvas = ROOT.gROOT.FindObject('c1')
		# canvas.Update()
		# raw_input('...')


class TrackAverager(object):
	def __init__(self, filename):
		super (TrackAverager, self).__init__()
		self.filename = filename

	def read_data(self):
		inlist = ROOT.TFile(self.filename).TrackAverages
		hist = lambda n: inlist.FindObject(n)
		nevents, tpc, emcal = map(hist, ['hEvents','hTracksTPC', 'hClustersEMCal'])

		return self.average(tpc, nevents), self.average(emcal, nevents)

	def average(self, hist, nevents):
		# Average
		hist.Divide(nevents)
		# Sort
		label_values = {int(hist.GetXaxis().GetBinLabel(i)): hist.GetBinContent(i) for i in range(1, hist.GetNbinsX())}
		average = hist.Clone('hAverage' + hist.GetName())
		average.SetTitle(hist.GetTitle().replace('Total', 'Average'))
		for i, k in enumerate(sorted(label_values)):
			average.SetBinContent(i + 1, label_values[k])
			average.GetXaxis().SetBinLabel(i + 1, str(k))
		return average

	def compare_to(self, filename):
		infile = ROOT.TFile(filename)
		mhsit = infile.Get('hAvNCluster_NC1_Emin=0.30GeV_corr4accept')
		canvas = ROOT.TCanvas('c1', 'test', 800, 500)
		canvas.Divide(1, 3)
		canvas.cd(1)
		mhsit.Draw()

		tpc, emcal = self.read_data()
		canvas.cd(2)
		tpc.Draw()
		tpc.GetXaxis().SetLabelSize(0.06)

		canvas.cd(3)
		emcal.Draw()
		emcal.GetXaxis().SetLabelSize(0.06)
		canvas.Update()
		raw_input('Press enter to continue')

  





def main():
	c = TrackAverager('TrackAverages.LHC16j-muon-calo-pass1.root')
	f = '../../results/LHC16j/iteration2/images/cluster-averages.move.root'
	c.compare_to(f)
	
if __name__ == '__main__':
	main()