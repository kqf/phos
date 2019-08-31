import ROOT

from operator import mul

import spectrum.sutils as su
from spectrum.broot import BROOT as br


class MassesPlot(object):

    def transform(self, imass, pad):
        self._evaluate(imass.mass, imass.sigf, imass.background, imass.signal,
                       imass.bgrf, imass.initial_fitting_region,
                       imass.integration_region, pad)

    def _evaluate(self, mass, sigf, background, signal, bgrf,
                  initial_fitting_region, integration_region, pad):
        su.ticks(pad)
        ci = br.define_colors()
        pad.cd()
        self._set_axis_limits(mass, signal, initial_fitting_region)
        self.draw(mass, "histe")
        self.draw(sigf, color=ci[1])
        self.draw(background, color=ci[1])
        self.draw(signal, color=ci[2])
        self.draw(bgrf, color=ci[5])
        self.draw_chisquare(sigf)
        self._draw_line(mass, *integration_region)
        pad.Update()

    def draw_chisquare(self, func):
        if not func:
            return
        latex = ROOT.TPaveText(.5, .5, .5, .5)
        latex.SetTextSize(10)
        latex.SetTextAlign(13)

        if func.GetNDF() > 0:
            chi2ndf = func.GetChisquare() / func.GetNDF()
            latex.AddText("#chi^{{2}} / ndf = {}".format(chi2ndf))
            latex.DrawClone("same")
            func.chi2ndf = chi2ndf
        return latex

    def draw(self, hist, option="same", color=1):
        if not hist:
            return
        hist.Draw(option)
        hist.SetMarkerColor(color)
        hist.SetLineColor(color)
        hist.SetFillColor(color)
        hist.SetFillStyle(0)
        return hist

    def _set_axis_limits(self, mass, signal, limits):
        mass.GetXaxis().SetRangeUser(*limits)
        yaxis = mass.GetYaxis()
        yaxis.SetTitle(
            "{}/{} MeV".format(yaxis.GetTitle(), mass.GetBinWidth(1) * 1000))

        def bins_errors(hist, a, b):
            bins, berrors, centers = br.bins(hist)
            roi = (centers > a) & (centers < b)
            bins = bins[roi]
            berrors = berrors[roi]
            return bins, berrors

        try:
            mbins, merrors = bins_errors(mass, *limits)
            sbins, serrors = bins_errors(signal, *limits)
        except:
            import ipdb; ipdb.set_trace()
        yaxis.SetRangeUser(
            min(sbins) - 2 * max(serrors),
            max(mbins) + 3 * max(merrors)
        )

    def _draw_line(self, mass, lower, upper):
        # Draw integration region, when specified
        def lline(pos):
            line = ROOT.TLine(pos, mass.GetMinimum(), pos, mass.GetMaximum())
            line.SetLineColor(1)
            line.SetLineStyle(7)
            line.Draw()
            return line
        # Dirty hack for root memory management
        mass.line_low = lline(lower)
        mass.line_upper = lline(upper)


class MultiplePlotter(object):
    def __init__(self):
        super(MultiplePlotter, self).__init__()
        self.multcanvas = [4, 3, 0.001, 0.001]
        self.lastcanvas = [2, 2, 0.001, 0.001]

    def transform(self, masses, show=False):
        self.all_bins(masses, show)

    def all_bins(self, masses, show):
        n_plots = mul(*self.multcanvas[0:2])
        for i in range(0, len(masses), n_plots):
            canvas = su.gcanvas(x=1, y=1, resize=True)
            canvas.Clear()
            canvas.Divide(*self.multcanvas)
            plotter = MassesPlot()
            for j, mass in enumerate(masses[i:i + n_plots]):
                plotter.transform(mass, canvas.cd(j + 1))
            canvas.Write("masses_{}".format(i))


class MulipleOutput(object):

    def __init__(self, masses):
        super(MulipleOutput, self).__init__()
        self.masses = masses

    def Write(self):
        for mass in self.masses:
            mass.mass.Write()

            if mass.ratio:
                mass.ratio.Write()

            if mass.background:
                mass.background.Write()

        MultiplePlotter().transform(self.masses)
