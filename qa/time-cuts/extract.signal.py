#!/usr/bin/python2

import numpy as np
import ROOT

ROOT.TH1.AddDirectory(False)

def wait(name = 'default', draw = True, save = False):
    canvas = ROOT.gROOT.FindObject('c1')
    canvas.Update()
    name = name.replace(' ', '_')
    if save: canvas.SaveAs('results/' + name+ '.pdf')

    canvas.Connect("Closed()", "TApplication", ROOT.gApplication, "Terminate()")
    if draw: ROOT.gApplication.Run(True)

def fit_function(h):
    f = ROOT.TF1('f1', 'gaus(0)', -0.1 * 1e-6, 0.1 * 1e-6)
    f.SetParameters(1.6e+06, 0, 2.1e-08)
    h.Fit(f, 'R')
    return f


class Analyser2D(object):
    def __init__(self, hist):
        super(Analyser2D, self).__init__()
        self.hist = hist 

    @staticmethod
    def from_file(filename):
        inlist = ROOT.TFile.Open(filename, 'r').PhysTender
        histogram = inlist.FindObject('hClusterEvsTM')
        return Analyser2D(histogram)

    def trim(self, threshold):
        for i in range(1, self.hist.GetXaxis().GetNbins()):
            for j in range(1, self.hist.GetYaxis().GetNbins()):
                if self.hist.GetBinContent(i, j) < threshold:
                    self.hist.SetBinContent(i, j, 0)
        return self.hist.Integral()

    def check_convergence(self, data):
        from array import array
        x, y, z = zip(*data)
        time = ROOT.TGraph(len(x), array('f', x), array('f', y))
        resolution = ROOT.TGraph(len(x), array('f', x), array('f', z))

        time.SetMarkerStyle(20)
        time.SetLineColor(37)
        time.Draw('ap')
        wait()

        resolution.SetMarkerStyle(20)
        resolution.SetLineColor(46)
        resolution.Draw('ap')
        wait()


    def estimate_cut(self):
        s = 200
        # TODO1: try this for the finer bins
        # TODO2: Approximate precision
        # TODO3: Additional histograms in example task?
        self.hist.SetAxisRange(-0.25 * 1e-6, 0.25* 1e-6, 'Y')

        data, initial = [], self.hist.Integral()
        for i in np.linspace(1e3, 6e4, 20):
            # canvas = ROOT.TCanvas('c1', 'test', 4 * s, 3 * s)
            # canvas.Divide(2, 1)
            x = self.trim(i) / initial
            # canvas.cd(1)
            # self.hist.Draw('colz')
            time = self.hist.ProjectionY()
            time.SetTitle('ToF distribution in all modules %d; t, s' %i)
            time.SetAxisRange(-0.25 * 1e-6, 0.25* 1e-6, 'X')
            # canvas.cd(2).SetLogy()
            f = fit_function(time)
            data.append([x, f.GetParameter(1), f.GetParameter(2)])
            time.Draw('same')
            # f.Draw('same')
            # wait()
        self.check_convergence(data)


def main():
    analyzer = Analyser2D.from_file("LHC16k-MyTask.root")
    analyzer.estimate_cut()


if __name__ == '__main__':
    main()

