import ROOT
import click
import numpy as np

ROOT.TH1.AddDirectory(False)
ROOT.gStyle.SetOptStat('erm')


def wait(name='default', draw=True, save=False):
    canvas = ROOT.gROOT.FindObject('c1')
    canvas.Update()
    name = name.replace(' ', '_')
    if save:
        canvas.SaveAs('results/' + name + '.pdf')

    canvas.Connect("Closed()", "TApplication",
                   ROOT.gApplication, "Terminate()")
    if draw:
        ROOT.gApplication.Run(True)


def fit_function(h):
    f = ROOT.TF1('f1', 'gaus(0)', -2 * 1e-8, 2 * 1e8)
    f.SetParameters(4.7e+03, 0, 2.8e-9)
    h.Fit(f, 'R')
    return f


class Analyser2D(object):
    def __init__(self, hist):
        super(Analyser2D, self).__init__()
        self.hist = hist

    @staticmethod
    def from_file(filename, i=0):
        inlist = ROOT.TFile.Open(filename, 'r').TimeTender
        histogram = inlist.FindObject('hClusterEvsTM%d' % i)
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
        self.hist.SetAxisRange(-0.25 * 1e-6, 0.25 * 1e-6, 'Y')

        data, initial = [], self.hist.Integral()
        for i in np.linspace(1e3, 6e4, 20):
            x = self.trim(i) / initial
            time = self.hist.ProjectionY()
            time.SetTitle('ToF distribution in all modules %d; t, s' % i)
            time.SetAxisRange(-0.25 * 1e-6, 0.25 * 1e-6, 'X')
            f = fit_function(time)
            data.append([x, f.GetParameter(1), f.GetParameter(2)])
            time.Draw('same')

        self.check_convergence(data)

    def check_distribution(self):
        s = 200
        self.hist.SetAxisRange(-0.25 * 1e-6, 0.25 * 1e-6, 'Y')

        canvas = ROOT.TCanvas('c1', 'test', 4 * s, 3 * s)
        canvas.Divide(2, 1)
        canvas.cd(1)
        self.hist.Draw('colz')

        canvas.cd(2).SetLogy()
        axis = self.hist.GetXaxis()
        a, b = axis.FindBin(2), axis.GetNbins() - 1
        time = self.hist.ProjectionY("_py", a, b)
        time.SetTitle('ToF distribution in all modules; t, s')
        time.SetAxisRange(-0.25 * 1e-6, 0.25 * 1e-6, 'X')

        f = fit_function(time)
        time.Draw('same')
        f.Draw('same')
        wait()

    def get_images(self):
        self.hist.SetAxisRange(-0.25 * 1e-6, 0.25 * 1e-6, 'Y')
        self.hist.Draw('colz')

        axis = self.hist.GetXaxis()
        a, b = axis.FindBin(2), axis.GetNbins() - 1
        time = self.hist.ProjectionY("_py", a, b)
        time.SetTitle('ToF distribution in all modules; t, s')
        time.SetAxisRange(-0.25 * 1e-6, 0.25 * 1e-6, 'X')
        return self.hist, time


@click.command()
@click.option('--filename', required=True)
def distribution(filename):
    analyzer = Analyser2D.from_file(filename)
    analyzer.check_distribution()


@click.command()
@click.option('--filename', required=True)
def main(filename):
    analyzers = [Analyser2D.from_file(filename, i + 1) for i in range(4)]
    energy, proj = zip(*[a.get_images() for a in analyzers])

    scale, rows = 8, 1
    canvas = ROOT.TCanvas('c1', 'Canvas', 128 * scale / rows, 96 * scale)
    canvas.Divide(2, 2)

    for i, e in enumerate(energy):
        canvas.cd(i + 1)
        e.SetTitle(e.GetTitle() + '; energy, GeV; time, s')
        e.Draw('colz')
    canvas.Update()
    canvas.SaveAs('energy-time.pdf')

    legend = ROOT.TLegend(0.9, 0.4, 1.0, 0.6)
    legend.SetBorderSize(0)
    legend.SetFillStyle(0)
    legend.SetTextSize(0.04)

    ROOT.gStyle.SetOptStat(0)
    canvas = ROOT.TCanvas('c2', 'Canvas', 128 * scale / rows, 96 * scale)
    canvas.cd()
    proj[0].Draw()
    colors = [37, 46, 8, 1]
    for i, (p, c) in enumerate(zip(proj, colors)):
        canvas.SetLogy()
        canvas.SetGridx()
        p.SetAxisRange(-0.15 * 1e-6, 0.15 * 1e-6, 'X')
        p.Draw('same')
        p.SetLineColor(c)
        legend.AddEntry(p, 'SM %d' % (i + 1))

    legend.Draw('same')
    canvas.SaveAs('time.pdf')
    canvas.Update()
    raw_input('...')


if __name__ == '__main__':
    main()
