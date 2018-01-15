import ROOT
import sutils as su

class PtPlotter(object):
    def __init__(self, masses, options, label):
        super(PtPlotter, self).__init__()
        self.masses = masses
        self.opt = options
        self.label = label

    def draw(self):
        self._draw_ratio()
        self._draw_mass()
        self._draw_signal()

    def _draw_last_bins(self, f, name = ''):
        canvas = su.gcanvas(1, 1, True)
        canvas.Clear()
        canvas.Divide(*self.opt.lastcanvas)
        for i, m in enumerate(self.masses[-4:]):
            distr = f(m, canvas.cd(i + 1))

            # Draw integration region, when specified
            lower, upper = m.integration_region
            m.line_low = self._draw_line(distr, lower)
            m.line_upper = self._draw_line(distr, upper)

        su.wait(name + self.label, self.opt.show_img, save=True)

    def _draw_all_bins(self, f, name = ''):
        canvas = su.gcanvas(1, 1, True)
        canvas.Clear()
        canvas.Divide(*self.opt.multcanvas)
        for i, m in enumerate(self.masses):
            distr = f(m, canvas.cd(i + 1))

            # Draw integration region, when specified
            lower, upper = m.integration_region
            m.line_low = self._draw_line(distr, lower)
            m.line_upper = self._draw_line(distr, upper)

        su.wait(name + self.label, self.opt.show_img, save=True)

    def _draw_ratio(self, name = ''):
        f = lambda x, y: x.draw_ratio(y)
        oname = 'multiple-ratio-{0}-{1}'.format(self.opt.particle, name)
        self._draw_all_bins(f, oname)

    def _draw_mass(self, name = ''):
        f = lambda x, y: x.draw_mass(y)
        oname = 'multiple-mass-{0}-{1}'.format(self.opt.particle, name)
        self._draw_all_bins(f, oname)

    def _draw_signal(self, name = ''):
        f = lambda x, y: x.draw_signal(y) 
        oname = 'multiple-signal-{0}-{1}'.format(self.opt.particle, name)
        self._draw_all_bins(f, oname)

        oname = 'multiple-signal-high-pt-{0}-{1}'.format(self.opt.particle, name)
        self._draw_last_bins(f, oname)

    def _draw_line(self, distr, position):
        if not distr:
            return
        line = ROOT.TLine(position, distr.GetMinimum(), position, distr.GetMaximum())
        line.SetLineColor(1)
        line.SetLineStyle(7)
        line.Draw()
        return line

        canvas.Divide(*self.opt.lastcanvas)