import ROOT
import sutils as su

class PtPlotter(object):
    def __init__(self, masses, options):
        super(PtPlotter, self).__init__()
        self.masses = masses
        self.opt = options

    def draw(self, intgr_ranges, draw):
        if not draw:
            return 
        self._draw_ratio(intgr_ranges)
        self._draw_mass(intgr_ranges)
        self._draw_signal(intgr_ranges)

    def _draw_last_bins(self, f, intgr_ranges, name = ''):
        canvas = su.gcanvas(1, 1, True)
        canvas.Clear()
        canvas.Divide(*self.opt.lastcanvas)
        for i, (m, r) in enumerate(zip(self.masses[-4:], intgr_ranges[-4:])):
            distr = f(m, canvas.cd(i + 1))

            # Draw integration region, when specified
            if not r: continue
            m.line_low = self._draw_line(distr, r[0])
            m.line_up = self._draw_line(distr, r[1])

        su.wait(name + self.opt.label, self.opt.show_img, save=True)

    def _draw_all_bins(self, f, intgr_ranges, name = ''):
        canvas = su.gcanvas(1, 1, True)
        canvas.Clear()
        canvas.Divide(*self.opt.multcanvas)
        for i, (m, r) in enumerate(zip(self.masses, intgr_ranges)):
            distr = f(m, canvas.cd(i + 1))

            # Draw integration region, when specified
            if not r: continue
            m.line_low = self._draw_line(distr, r[0])
            m.line_up = self._draw_line(distr, r[1])

        su.wait(name + self.opt.label, self.opt.show_img, save=True)

    def _draw_ratio(self, intgr_ranges, name = ''):
        f = lambda x, y: x.draw_ratio(y)
        oname = 'multiple-ratio-{0}-{1}'.format(self.opt.particle, name)
        self._draw_all_bins(f, intgr_ranges, oname)

    def _draw_mass(self, intgr_ranges, name = ''):
        f = lambda x, y: x.draw_mass(y)
        oname = 'multiple-mass-{0}-{1}'.format(self.opt.particle, name)
        self._draw_all_bins(f, intgr_ranges, oname)

    def _draw_signal(self, intgr_ranges, name = ''):
        f = lambda x, y: x.draw_signal(y) 
        oname = 'multiple-signal-{0}-{1}'.format(self.opt.particle, name)
        self._draw_all_bins(f, intgr_ranges, oname)

        oname = 'multiple-signal-high-pt-{0}-{1}'.format(self.opt.particle, name)
        self._draw_last_bins(f, intgr_ranges, oname)

    def _draw_line(self, distr, position):
        if not distr:
            return
        line = ROOT.TLine(position, distr.GetMinimum(), position, distr.GetMaximum())
        line.SetLineColor(1)
        line.SetLineStyle(7)
        line.Draw()
        return line

        canvas.Divide(*self.opt.lastcanvas)