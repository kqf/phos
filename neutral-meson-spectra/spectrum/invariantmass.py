from __future__ import print_function

import humanize
from spectrum.broot import BROOT as br
from spectrum.parametrisation import parametrisation
from spectrum.constants import PAVE_PREFIX


def masses2edges(masses):
    return sorted(set(
        sum([list(i.pt_range) for i in masses], [])
    ))


class RawMass(object):

    reactions = {
        "#pi^{0}": "#pi^{0} #rightarrow #gamma #gamma",
        "#eta": "#eta #rightarrow #gamma #gamma",
        "electrons": "e^{#pm}",
    }

    xaxes = {
        "#pi^{0}": "M_{#gamma#gamma}, GeV/c^{2}",
        "#eta": "M_{#gamma#gamma}, GeV/c^{2}",
        "electrons": "E/p ratio",
    }

    def __init__(self, inhists, pt_range, nrebin, particle, pt_interval):
        self.pt_interval = pt_interval
        self.pt_range = pt_range
        self.nrebin = nrebin
        self.particle = particle
        label = "{:.4g} < p_{{T}} < {:.4g} GeV/c"
        self.pt_label = label.format(*self.pt_range)
        self.template = "{pref} | {reaction} | {pt} | N_{{events}} = {events}"
        self.mass, self.background = map(self._extract_histogram, inhists)

    def _extract_histogram(self, hist):
        if not hist:
            return None
        return self.read_mass(
            hist, self.pt_range, self.nrebin, self.pt_interval)

    def read_mass(self, hist, pt_range, nrebin, pt_interval):
        mass = br.project_range(hist, "_%d_%d", *pt_range)
        mass.nevents = hist.nevents
        title = self.template.format(
            pref=PAVE_PREFIX,
            reaction=self.reactions[self.particle],
            pt=self.pt_label,
            events=humanize.intword(mass.nevents)
        )
        mass.SetTitle(title)
        mass.GetXaxis().SetTitle(self.xaxes[self.particle])
        mass.GetYaxis().SetTitle("counts")
        mass.SetLineColor(37)

        if not mass.GetSumw2N():
            mass.Sumw2()

        if nrebin:
            mass.Rebin(nrebin)
        return mass


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
