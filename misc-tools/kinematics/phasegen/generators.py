import array
from math import sqrt

import numpy as np
import ROOT


class EventGenerator(object):
    def __init__(self, function, original_mass, decay_masses):
        super(EventGenerator, self).__init__()
        self.function = function
        self.original_mass = original_mass
        self.decay_masses = array.array('d', decay_masses)

    def event(self):
        particle, out = self._generate_original(), self.decay_masses
        event = ROOT.TGenPhaseSpace()
        event.SetDecay(particle, len(out), out)
        event.Generate()
        return [event.GetDecay(i) for i in range(len(out))], particle

    def _generate_original(self):
        p = self.function.GetRandom()
        energy = sqrt(self.original_mass ** 2 + p ** 2)
        return ROOT.TLorentzVector(0., 0., p, energy)


class EventGeneratorRandomized(EventGenerator):
    def _generate_original(self):
        p = self.function.GetRandom()
        mass = np.random.normal(self.original_mass, 0.01)
        energy = sqrt(mass ** 2 + p ** 2)
        return ROOT.TLorentzVector(0., 0., p, energy)
