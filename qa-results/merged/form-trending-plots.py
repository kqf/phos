#!/usr/bin/python



import ROOT 
import subprocess, sys

def get_runs(fname):
	mfile = ROOT.TFile.Open(fname)
	names = [ key.GetName() for key in mfile.PHOSCellsQA if 'Pi0' in key.GetName() ]
	names = set([n.split('_')[0].replace('run', '') for n in names])
	runs = [int(i) for i in names ]
	runNumbers = [236137, 236138, 236150, 236151, 236153, 236158, 236161, 236163, 236204, 236222, 236227, 236234, 236238, 236240, 236242, 236244, 236246, 236248, 236348, 236349, 236352, 236353, 236354, 236356, 236359, 236389, 236393, 236441, 236443, 236444, 236556, 236558, 236562, 236563, 236564, 236565, 236813, 236814, 236815, 236816, 236821, 236824, 236835, 236848, 236850, 236860, 236862, 236863, 236866]

	if len(runs) != len(runNumbers): print 'ERROR: Remove this for another run'
	return runs


def main():
	path = sys.argv[1] + '/'
	ifile = 'CaloCellsQASingle.root'
	filename = path + ifile

	print 'Reading', filename

	runNumbers = get_runs(filename)
	ROOT.gROOT.LoadMacro("MakeTrendingPHOSQA.C")

	for run in runNumbers:
		res = subprocess.call("root -l -q -b 'MakeTrendingPHOSQA.C(\"%s\", \"%s\", %d)'" %(path, ifile, run), shell=True)  
		# ROOT.MakeTrendingPHOSQAE(path, ifile, run)

	files = ['%strending' % path + str(r) + '.root' for r in runNumbers]
	subprocess.call("rm %strending.root" % path, shell=True)  
	subprocess.call("hadd %strending.root " % path + ' '.join(files), shell=True)  
	subprocess.call("rm " + ' '.join(files), shell=True)  

	ROOT.gROOT.LoadMacro("DrawTrendingPHOSQA.C")
	ROOT.DrawTrendingPHOSQA(path + 'trending.root')


if __name__ == '__main__':
	main()


