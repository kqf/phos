import ROOT
import sutils as su
from broot import BROOT as br
from operator import mul


class MassesPlot(object):

    def transform(self, imass, pad):
        su.ticks(pad)
        if not imass.signal:
            return

        ci = br.define_colors()
        pad.cd()

        self._set_axis_limits(imass)
        self.draw(imass.mass, "histe")
        if imass.sigf:
            imass.sigf.SetLineStyle(9)
        self.draw(imass.sigf, color=ci[1])
        self.draw(imass.background, color=ci[1])
        self.draw(imass.signal, color=ci[2])
        self.draw(imass.bgrf, color=ci[5])
        self.draw_chisquare(imass.sigf)
        self._draw_line(imass)
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

    def _set_axis_limits(self, imass):
        a, b = imass.initial_fitting_region
        imass.mass.GetXaxis().SetRangeUser(a, b)
        ytitle = imass.mass.GetYaxis().GetTitle()
        imass.mass.GetYaxis().SetTitle(
            "{0}/{1} MeV".format(
                ytitle,
                imass.mass.GetBinWidth(1) * 1000
            )
        )

        def bins_errors(hist):
            bins, berrors, centers = br.bins(hist)
            roi = (centers > a) & (centers < b)
            bins = bins[roi]
            berrors = berrors[roi]
            return bins, berrors

        mbins, merrors = bins_errors(imass.mass)
        sbins, serrors = bins_errors(imass.signal)

        imass.mass.GetYaxis().SetRangeUser(
            min(sbins) - 2 * max(serrors),
            max(mbins) + 3 * max(merrors)
        )

    def _draw_line(self, imass):
        def lline(position):
            line = ROOT.TLine(position, imass.mass.GetMinimum(),
                              position, imass.mass.GetMaximum())
            line.SetLineColor(1)
            line.SetLineStyle(7)
            line.Draw()
            return line
            # Draw integration region, when specified
        lower, upper = imass.integration_region
        imass.line_low = lline(lower)
        imass.line_upper = lline(upper)


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
