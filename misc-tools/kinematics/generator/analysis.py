import json

import ROOT
import tqdm
from generator.generator import EventGeneratorRandomized


class AnalysisOptions(object):
    def __init__(self, cfile="config/angle-analysis.json"):
        super(AnalysisOptions, self).__init__()
        with open(cfile) as f:
            self.conf = json.load(f)
        self.n_events = self.conf["n_events"]
        self.generator = self.conf["generator"]
        self.type = EventGeneratorRandomized

        # Setup the momentum generation function
        momentum = self.conf["momentum_distribution"]
        function = ROOT.TF1('fPt', *momentum["function"])
        function.SetParameters(*momentum["parameters"])
        self.generator["function"] = function


class Analysis(object):
    def __init__(self, config=AnalysisOptions()):
        super(Analysis, self).__init__()
        self.n_events = config.n_events
        self.generator = config.type(**config.generator)

    def transform(self, selections):
        for _ in tqdm.trange(self.n_events):
            particles = self.generator.event()
            for selection in selections:
                selection.transform(particles)
