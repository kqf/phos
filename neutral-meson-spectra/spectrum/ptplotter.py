import ROOT
import sutils as su


class PtPlotterConfig(object):

    def __init__(self, particle):
        super(PtPlotterConfig, self).__init__()
        self.particle = particle
        init = self._init_pi0 if self.is_pi0(particle) else self._init_eta
        init()

    def _init_pi0(self):
        self.multcanvas = [6, 6, 0, 0.01]
        self.lastcanvas = [2, 2, 0.001, 0.01]
        self.partlabel = "#pi^{0}"

    def _init_eta(self):
        self.multcanvas = [4, 3, 0.001, 0.01]
        self.lastcanvas = [2, 2, 0.001, 0.01]
        self.partlabel = "#eta"

    def is_pi0(self, particle):
        pi0 = "#pi^{0}", "pi0"
        return particle in pi0


class PtPlotter(PtPlotterConfig):

    def __init__(self, masses, label, particle):
        super(PtPlotter, self).__init__(particle)
        self.masses = masses
        self.label = label

    def draw(self, stop, directory):
        self._draw_ratio(stop, directory)
        self._draw_mass(stop, directory)
        self._draw_signal(stop, directory)

    def _draw_last_bins(self, f, show, name):
        canvas = su.gcanvas(1, 1, True)
        canvas.Clear()
        canvas.Divide(*self.lastcanvas)
        for i, m in enumerate(self.masses[-4:]):
            distr = f(m, canvas.cd(i + 1))

            # Draw integration region, when specified
            lower, upper = m.integration_region
            m.line_low = self._draw_line(distr, lower)
            m.line_upper = self._draw_line(distr, upper)

        su.wait(name, draw=show, save=True)

    def _draw_all_bins(self, f, show, name):
        canvas = su.gcanvas(1, 1, True)
        canvas.Clear()
        canvas.Divide(*self.multcanvas)
        for i, m in enumerate(self.masses):
            distr = f(m, canvas.cd(i + 1))

            # Draw integration region, when specified
            lower, upper = m.integration_region
            m.line_low = self._draw_line(distr, lower)
            m.line_upper = self._draw_line(distr, upper)

        su.wait(name, draw=show, save=True)

    def _draw_ratio(self, show, directory):
        f = lambda x, y: x.draw_ratio(y)
        oname = '{1}/multiple-ratio-{0}'.format(self.particle, directory)
        self._draw_all_bins(f, show, oname)

    def _draw_mass(self, show, directory):
        f = lambda x, y: x.draw_mass(y)
        oname = '{1}/multiple-mass-{0}'.format(self.particle, directory)
        self._draw_all_bins(f, show, oname)

    def _draw_signal(self, show, directory):
        f = lambda x, y: x.draw_signal(y) 
        oname = '{1}/multiple-signal-{0}'.format(self.particle, directory)
        self._draw_all_bins(f, show, oname)

        oname = '{1}/multiple-signal-high-pt-{0}'.format(self.particle, directory)
        self._draw_last_bins(f, show, oname)

    def _draw_line(self, distr, position):
        if not distr:
            return
            
        line = ROOT.TLine(position, distr.GetMinimum(), position, distr.GetMaximum())
        line.SetLineColor(1)
        line.SetLineStyle(7)
        line.Draw()
        return line

        canvas.Divide(*self.lastcanvas)