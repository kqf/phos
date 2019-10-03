from __future__ import print_function

import humanize
from spectrum.broot import BROOT as br
from spectrum.parametrisation import parametrisation
from spectrum.constants import PAVE_PREFIX


def masses2edges(masses):
    return sorted(set(
        sum([list(i.pt_range) for i in masses], [])
    ))


def read_mass(hist, pt_range, nrebin, title, pt_interval):
    pt_label = '%.4g < p_{T} < %.4g' % pt_range
    mass = br.project_range(hist, '_%d_%d', *pt_range)
    mass.nevents = hist.nevents
    title = PAVE_PREFIX + title + "| {} GeV/c |".format(pt_label)
    title_stat = ' '
    if mass.nevents > 0:
        title_stat = "#events = {}".format(humanize.intword(mass.nevents))
    title_axes_labels = '; M_{#gamma#gamma}, GeV/c^{2}'
    mass.SetTitle(title + title_stat + title_axes_labels)
    mass.SetLineColor(37)

    if not mass.GetSumw2N():
        mass.Sumw2()

    if nrebin:
        mass.Rebin(nrebin)
    return mass


class RawMass(object):

    def __init__(self, inhists, pt_range, nrebin, title, pt_interval):
        self.pt_interval = pt_interval
        self.pt_range = pt_range
        self.nrebin = nrebin
        self.title = title
        self.pt_label = '%.4g < p_{T} < %.4g' % self.pt_range
        self.mass, self.background = map(self._extract_histogram, inhists)

    def _extract_histogram(self, hist):
        if not hist:
            return None
        return read_mass(
            hist, self.pt_range, self.nrebin, self.title, self.pt_interval)


class InvariantMass(object):

    def __init__(self, rmass, options):
        super(InvariantMass, self).__init__()
        self.opt = options
        self.mass = rmass.mass
        self.background = rmass.background
        self.pt_range = rmass.pt_range
        self.pt_label = rmass.pt_label
        self.pt_interval = rmass.pt_interval

        # Setup the fit function
        self._signal = parametrisation(options.signal)
        self._background = parametrisation(options.background)
        self.fit_range = self._signal.opt.fit_range

        # Extract the data
        self.sigf = None
        self.bgrf = None
        self.area_error = None
        self._integration_region = self._signal.opt.fit_range
        self.ratio = None
        self.signal = None
        self.background_fitted = None

    @property
    def integration_region(self):
        return self._integration_region

    @integration_region.setter
    def integration_region(self, value):
        if not value:
            return
        self._integration_region = value

    def number_of_mesons(self):
        # print(self.integration_region)
        # self.integration_region = (0.08, 0.2)
        area, areae = br.area_and_error(self.signal, *self.integration_region)
        # self.area_error = area, areae
        # return self.signal.Integral(), self.signal.GetEntries() ** 0.5
        return area, areae

    def fitted(self):
        return self.bgrf and self.sigf
