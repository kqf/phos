#!/usr/bin/python


import ROOT
import pickle

def main():
	data = pickle.load(open('noisy.pkl'))
	hist = ROOT.TH1F('Noise', 'Noise; # of runs a cell was noisy; Count', 27, 0, 27)
	for v in data.values(): hist.Fill(v)

	hist.Draw()
	canvas = ROOT.gROOT.FindObject('c1')
	canvas.Update()
	raw_input()


	result = [k for k in data if data[k] > 6]
	print ','.join(map(str, result))


if __name__ == '__main__':
	main()