#!/usr/bin/python

import ROOT

ROOT.TH1.AddDirectory(False)


def draw_histogram(hist, pad):
	hist.Draw()
	pad.SetLeftMargin(0.04);
	pad.SetRightMargin(0.02);
	pad.SetTopMargin(0.10);
	pad.SetBottomMargin(0.14);
	pad.SetTickx()
	pad.SetTicky() 
	pad.SetGridy()
	pad.SetGridx()


class TrackAverager(object):
	def __init__(self, filename_tracks, filename_clusters):
		super (TrackAverager, self).__init__()
		self.filename_tracks = filename_tracks
		self.filename_clusters = filename_clusters

	def read_data(self):
		# First extract PHOS average
		phos = ROOT.TFile(self.filename_clusters).Get('hAvNCluster_NC1_Emin=0.30GeV_corr4accept')

		# Then TPC/EMCal averages
		inlist = ROOT.TFile(self.filename_tracks).TrackAverages
		hist = lambda n: inlist.FindObject(n)

		nevents = hist('hEvents')
		hists = map(hist, ['hTracksTPC', 'hHybridTPC', 'hComplementaryTPC', 'hClustersEMCal'])
		return [phos] + map(lambda x: self.average(x, nevents, phos), hists)

	def average(self, hist, nevents, canonical):
		# Average
		print hist.GetName()
		hist.Divide(nevents)
		label = lambda h, i: h.GetXaxis().GetBinLabel(i)

		label_values = {label(hist, i): hist.GetBinContent(i) for i in range(1, hist.GetNbinsX())}
		average = canonical.Clone(hist.GetName() + canonical.GetName())
		average.Reset()

		for i in range(1, canonical.GetNbinsX()):
			labeli = label(canonical, i)
			if labeli in label_values:
				average.SetBinContent(i, label_values[labeli])

		maximum = max(label_values.values())
		average.SetAxisRange(maximum * 0.7, maximum * 1.1, "Y");
		average.SetTitle(hist.GetTitle().replace('Total', 'Average'))
		return average

	def compare(self):
		ROOT.gStyle.SetOptStat('')
		canvas = ROOT.TCanvas('c1', 'test', 128 * 6, 96 * 6)

		phos, tpc, hybrid, compl, emcal = self.read_data()

		canvas.Divide(1, 3)
		draw_histogram(phos, canvas.cd(1))
		# mhsit.Draw()

		tpc.GetYaxis().SetTitle('Number of TPC tracks')

		tpc.SetLineColor(38)
		hybrid.SetLineColor(42)
		compl.SetLineColor(8)

		draw_histogram(tpc, canvas.cd(2))
		hybrid.Draw("same")
		compl.Scale(20)
		compl.Draw("same")

		legend = ROOT.TLegend(0.6, 0.65, 0.85, 0.9)
		legend.SetFillStyle(0)
		legend.SetBorderSize(0)
		legend.AddEntry(tpc, "all tracks")
		legend.AddEntry(hybrid, "hybird tracks")
		legend.AddEntry(compl, "complementary tracks x 20")
		legend.Draw("same")

		emcal.GetYaxis().SetTitle('Number of EMCal clusters')
		draw_histogram(emcal, canvas.cd(3))
		canvas.Update()
		canvas.SaveAs('track-averages.pdf')
		raw_input('Press enter to continue')


def main():
	f = '../../results/LHC16k/iteration11/images/cluster-averages.move.root'
	c = TrackAverager('TrackAverages.LHC16k-pass1.root', f)
	c.compare()
	
if __name__ == '__main__':
	main()