from __future__ import print_function
import ROOT

import humanize
import spectrum.broot as br
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

    xaxis = {
        "#pi^{0}": "M_{#gamma#gamma} (GeV/#it{c}^{2})",
        "#eta": "M_{#gamma#gamma} (GeV/#it{c}^{2})",
        "electrons": "E/p ratio",
    }

    def __init__(self, pt_range, nrebin, particle, pt_interval):
        self.pt_interval = pt_interval
        self.pt_range = pt_range
        self.nrebin = nrebin
        self.particle = particle
        label = "{:.4g} < p_{{T}} < {:.4g} GeV/#it{{c}}"
        self.pt_label = label.format(*self.pt_range)
        self.template = "{pref} | {reaction} | {pt} | N_{{events}} = {events}"

    def transform(self, hist):
        if not hist:
            return None
        return self.read_mass(
            hist, self.pt_range, self.nrebin, self.pt_interval)

    def read_mass(self, hist, pt_range, nrebin, pt_interval):
        mass = br.project_range(hist, *pt_range)
        mass.nevents = hist.nevents
        title = self.template.format(
            pref=PAVE_PREFIX,
            reaction=self.reactions[self.particle],
            pt=self.pt_label,
            events=humanize.intword(mass.nevents)
        )
        mass.SetTitle(title)
        mass.GetXaxis().SetTitle(self.xaxis[self.particle])
        mass.GetYaxis().SetTitle("counts")
        mass.SetLineColor(ROOT.kRed + 1)

        if not mass.GetSumw2N():
            mass.Sumw2()

        if nrebin:
            mass.Rebin(nrebin)
        return mass


class InvariantMass(object):

    def __init__(self, rmass, options):
        super(InvariantMass, self).__init__()
        self.opt = options
        # self.mass = rmass.mass
        # self.background = rmass.background
        self.pt_range = rmass.pt_range
        self.pt_label = rmass.pt_label
        self.pt_interval = rmass.pt_interval

        # Setup the fit function
        # _signal = measured - combinatorial background = signal + residual
        self._signal = parametrisation(options.signal)

        # _measured distribution = signal + combinatorial background
        self._measured = parametrisation(options.background)
        self.fit_range = self._signal.opt.fit_range

        # Extract the data
        self.signalf = None
        self.bgrf = None
        self.area_error = None
        self._integration_region = self._signal.opt.fit_range
        self.ratio = None
        self.signal = None
        self.measuredf = None

    @property
    def mass(self):
        raise IOError("No such attribute")

    @property
    def background(self):
        raise IOError("No such attribute")

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
        return self.bgrf and self.signalf
