import ROOT

from operator import mul

import spectrum.sutils as su
import spectrum.broot as br
from repoze.lru import lru_cache


# TODO: Fix the name of the parameters in the signature for this method
# TODO: Fix the tests
class MassesPlot(object):

    def transform(self, mass, signalf, background, signal, measured,
                  fit_range, integration_region, pad):
        su.ticks(pad)
        pad.cd()

        title = mass.GetTitle()
        if mass is not None:
            mass.SetTitle("")
            # mass.SetStats(False)

        if signal is not None:
            signal.SetTitle("")
            # signal.SetStats(False)

        self._set_axis_limits(mass, signal, fit_range)
        self.draw(mass, "histe")
        self.draw(signal, color=br.BR_COLORS[2])
        self.draw(signalf, color=br.BR_COLORS[1])
        self.draw(background, color=br.BR_COLORS[1])
        self.draw(measured, color=br.BR_COLORS[5])
        self.draw_chisquare(signalf)
        self._line(mass, *integration_region).Draw()
        self._draw_text(title)
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

        def bins_errors(hist, a, b):
            bins, berrors, centers, _ = br.bins(hist)
            roi = (centers > a) & (centers < b)
            bins = bins[roi]
            berrors = berrors[roi]
            return bins, berrors

        mbins, merrors = bins_errors(mass, *limits)
        sbins, serrors = bins_errors(signal, *limits)

        yaxis.SetRangeUser(
            min(sbins) - 1 * max(serrors),
            max(mbins) + 4 * max(merrors)
        )

    @lru_cache(maxsize=1024)
    def _draw_line(self, mass, lower, upper):
        # Draw integration region, when specified
        def lline(pos):
            line = ROOT.TLine(pos, mass.GetMinimum(), pos, mass.GetMaximum())
            line.SetLineColor(1)
            line.SetLineStyle(7)
            line.Draw()
            return line
        # Dirty hack for root memory management
        return lline(lower), lline(upper)

    @lru_cache(maxsize=1024)
    def _draw_text(self, title, sep="|"):
        pave = ROOT.TPaveText(0.18, 0.75, 0.38, 0.88, "NDC")
        entries = title.split(sep)
        for entry in entries:
            if "event" in entry:
                continue
            pave.AddText(entry)
        pave.SetMargin(0)
        pave.SetBorderSize(0)
        pave.SetFillStyle(0)
        pave.SetTextAlign(13)
        pave.SetTextFont(42)
        pave.Draw()
        return pave


class MultiplePlotter(object):
    widths = [0.001, 0.001]
    layouts = {
        1: [1, 1],
        2: [2, 1],
        3: [3, 1],
        4: [2, 2],
        5: [3, 2],
        6: [3, 2],
        9: [3, 3],
    }
    default = [4, 3]

    def transform(self, masses, stop=False):
        canvas_shape = self.layouts.get(len(masses), self.default)
        n_plots = mul(*canvas_shape)
        for i in range(0, len(masses), n_plots):
            with su.canvas(stop=stop) as canvas:
                canvas.Clear()
                canvas.Divide(*canvas_shape + self.widths)
                plotter = MassesPlot()
                for j, mass in enumerate(masses[i:i + n_plots]):
                    plotter.transform(
                        pad=canvas.cd(j + 1),
                        mass=mass["signal"],
                        signalf=mass["signalf"],
                        background=mass["background"],
                        signal=mass["signal"],
                        measured=mass["measured"],
                        fit_range=mass["fit_range"],
                        integration_region=mass["integration_region"],
                    )
                canvas.Write("masses_{}".format(i))


class MulipleOutput(object):

    def __init__(self, masses):
        super(MulipleOutput, self).__init__()
        self.masses = masses

    def Write(self):
        MultiplePlotter().transform(self.masses)

        with br.tdirectory("raw"):
            for mass in self.masses:
                mass["signal"].Write()
                mass["measured"].Write()
                # TODO: Save the ratio as well
                # mass["ratio"].Write()
                mass["background"].Write()
