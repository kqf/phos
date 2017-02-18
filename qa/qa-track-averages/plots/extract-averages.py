#!/usr/bin/python

import ROOT


def draw_histogram(hist, pad):
    hist.Draw()
    pad.SetTickx()
    pad.SetTicky() 
    pad.SetGridy()
    pad.SetGridx()


class TrackAverager(object):
	def __init__(self, filename):
		super (TrackAverager, self).__init__()
		self.filename = filename

	def read_data(self):
		inlist = ROOT.TFile(self.filename).TrackAverages
		hist = lambda n: inlist.FindObject(n)
		nevents, tpc, hybrid, compl, emcal = map(hist, ['hEvents', 'hTracksTPC', 'hHybridTPC', 'hComplementaryTPC', 'hClustersEMCal'])

		return self.average(tpc, nevents), self.average(hybrid, nevents), self.average(compl, nevents), self.average(emcal, nevents), 

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
		ROOT.gStyle.SetOptStat('')
		infile = ROOT.TFile(filename)
		mhsit = infile.Get('hAvNCluster_NC1_Emin=0.30GeV_corr4accept')
		canvas = ROOT.TCanvas('c1', 'test', 128 * 6, 96 * 6)

		canvas.Divide(1, 3)
		draw_histogram(mhsit, canvas.cd(1))
		# mhsit.Draw()

		tpc, hybrid, compl, emcal = self.read_data()
		tpc.GetXaxis().SetLabelSize(0.06)
		tpc.GetYaxis().SetTitleSize(0.06)
		tpc.GetYaxis().SetTitleOffset(0.3)
		tpc.GetYaxis().SetTitle('Number of TPC tracks')

		tpc.SetLineColor(38)
		hybrid.SetLineColor(42)
		compl.SetLineColor(8)

		draw_histogram(tpc, canvas.cd(2))
		hybrid.Draw("same")
		compl.Draw("same")

		legend = ROOT.TLegend(0.6, 0.65, 0.85, 0.9)
		legend.SetFillStyle(0)
		legend.SetBorderSize(0)
		legend.AddEntry(tpc, "all tracks")
		legend.AddEntry(hybrid, "hybird tracks")
		legend.AddEntry(compl, "complementary tracks")
		legend.Draw("same")


		
		emcal.GetXaxis().SetLabelSize(0.06)
		emcal.GetYaxis().SetTitleSize(0.06)
		emcal.GetYaxis().SetTitleOffset(0.3)
		emcal.GetYaxis().SetTitle('Number of EMCal clusters')
		draw_histogram(emcal, canvas.cd(3))
		canvas.Update()
		canvas.SaveAs('track-averages.pdf')
		raw_input('Press enter to continue')

  





def main():
	c = TrackAverager('TrackAverages.LHC16k-pass1.root')
	f = '../../results/LHC16k/iteration11/images/cluster-averages.move.root'
	c.compare_to(f)
	
if __name__ == '__main__':
	main()