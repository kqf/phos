import array
import json
from math import pi, sqrt

import ROOT
import tqdm


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


class AnalysisOptions(object):
    def __init__(self, cfile="config/angle-analysis.json"):
        super(AnalysisOptions, self).__init__()
        with open(cfile) as f:
            self.conf = json.load(f)
        self.n_events = self.conf["n_events"]
        self.generator = self.conf["generator"]

        # Setup the momentum generation function
        momentum = self.conf["momentum_distribution"]
        function = ROOT.TF1('fPt', *momentum["function"])
        function.SetParameters(*momentum["parameters"])
        self.generator["function"] = function


class Analysis(object):
    def __init__(self, config=AnalysisOptions()):
        super(Analysis, self).__init__()
        self.n_events = config.n_events
        self.generator = EventGenerator(**config.generator)

    def transform(self, selections):
        for _ in tqdm.trange(self.n_events):
            particles = self.generator.event()
            for selection in selections:
                selection.transform(particles)


class AngleSelection(object):
    def __init__(self, ofile="output.root"):
        super(AngleSelection, self).__init__()
        self.ofile = ofile
        title = "Opening angle between two photons; #theta, rad"
        self.angle = ROOT.TH1F("hAngle", title, 10000, 0, pi / 2)
        title = "Opening angle between two photons vs momentum"
        title += "; #theta, rad; p, GeV/c"
        self.angle_p = ROOT.TH2F(
            "hAngleMomentum", title, 5000, 0, pi / 2, 1000, 15, 100)
        self.original = ROOT.TH1F("hP", "", 1000, 15, 100)

    def transform(self, particles):
        (first, second), original = particles
        angle = first.Angle(second.Vect())
        self.angle.Fill(angle)
        self.angle_p.Fill(angle, original.P())
        self.original.Fill(original.P())

    def write(self):
        ofile = ROOT.TFile(self.ofile, "recreate")
        self.angle.Write()
        self.angle_p.Write()
        self.original.Write()
        ofile.Close()