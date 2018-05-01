#!/usr/bin/python

from parametrisation import PeakParametrisation
from broot import BROOT as br


class RawMass(object):

    def __init__(self, inhists, pt_range, nrebin):
        self.pt_range = pt_range
        self.nrebin = nrebin
        self.pt_label = '%.4g < p_{T} < %.4g' % self.pt_range
        self.mass, self.background = map(self._extract_histogram, inhists)

    def _extract_histogram(self, hist):
        if not hist:
            return None
        mass = br.project_range(hist, '_%d_%d', *self.pt_range)
        mass.nevents = hist.nevents
        mass.SetTitle(
            self.pt_label + '  #events = %d M; M_{#gamma#gamma}, GeV/c^{2}' % (mass.nevents / 1e6))
        mass.SetLineColor(37)

        if not mass.GetSumw2N():
            mass.Sumw2()

        if self.nrebin:
            mass.Rebin(self.nrebin)
        return mass

    @staticmethod
    def ptedges(masses):
        return sorted(set(
            sum([list(i.pt_range) for i in masses], [])
        ))


class InvariantMass(object):

    def __init__(self, rmass, options):
        super(InvariantMass, self).__init__()
        self.opt = options
        self.mass = rmass.mass
        self.background = rmass.background
        self.pt_range = rmass.pt_range
        self.pt_label = rmass.pt_label

        # Setup the fit function
        self.signalp = PeakParametrisation.get(options.signalp)
        self.backgroundp = PeakParametrisation.get(options.backgroundp)
        # TODO: Remove offsets
        self.xaxis_range = [
            i * j for i, j in zip(
                self.signalp.opt.fit_range,
                self.opt.xaxis_offsets)
        ]

        # Extract the data
        self.sigf = None
        self.bgrf = None
        self.area_error = None
        self.initial_fitting_region = self.signalp.opt.fit_range
        self._integration_region = self.signalp.opt.fit_range
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
        # assert value[0] > 0, "Trying to set negative values {0}".format(value)

        self._integration_region = value

    def number_of_mesons(self):
        # print self.integration_region
        # self.integration_region = (0.08, 0.2)
        area, areae = br.area_and_error(self.signal, *self.integration_region)
        # self.area_error = area, areae
        # return self.sigf.Integral(*self.integration_region), 0 * self.signal.GetEntries() ** 0.5
        # return self.signal.Integral(), self.signal.GetEntries() ** 0.5
        return area, areae

    def fitted(self):
        return self.bgrf and self.sigf
