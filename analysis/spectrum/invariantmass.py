from __future__ import print_function
import ROOT

import humanize
import spectrum.broot as br
from spectrum.parametrisation import parametrisation
from spectrum.constants import PAVE_PREFIX


class RawMass(object):

    reactions = {
        "#pi^{0}": "#pi^{0} #rightarrow #gamma #gamma",
        "#eta": "#eta #rightarrow #gamma #gamma",
        "electrons": "#it{e}^{#pm}",
    }

    xaxis = {
        "#pi^{0}": "#it{M}_{#gamma#gamma} (GeV/#it{c}^{2})",
        "#eta": "#it{M}_{#gamma#gamma} (GeV/#it{c}^{2})",
        "electrons": "#it{E}/#it{p} ratio",
    }

    def __init__(self, pt_range, nrebin, pt_label, particle):
        self.pt_range = pt_range
        self.nrebin = nrebin
        self.particle = particle
        self.pt_label = pt_label

    def transform(self, hist):
        if not hist:
            return None
        return self.read_mass(
            hist, self.pt_range, self.nrebin,
            self.pt_label, self.particle)

    def read_mass(self, hist, pt_range, nrebin, pt_label, particle):
        mass = br.project_range(hist, *pt_range)
        mass.nevents = hist.nevents
        title = (
            "{prefix} "
            "| {reaction} "
            "| {pt} "
            "| #it{{N}}_{{events}} = {events}"
        ).format(
            prefix=PAVE_PREFIX,
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

    def __init__(self, options):
        super(InvariantMass, self).__init__()
        self.opt = options

        # Setup the fit function
        # _signal = measured - combinatorial background = signal + residual
        self._signal = parametrisation(options.signal)

        # _measured distribution = signal + combinatorial background
        self._measured = parametrisation(options.background)
        self.fit_range = self._signal.opt.fit_range

    @property
    def mass(self):
        raise IOError("No such attribute")

    @property
    def background(self):
        raise IOError("No such attribute")

    @property
    def integration_region(self):
        raise IOError("No such attribute")

    @integration_region.setter
    def integration_region(self, value):
        raise IOError("No such attribute")

    def number_of_mesons(self):
        raise IOError("No such attribute")

    def fitted(self):
        return self.bgrf and self.signalf
