import json
import ROOT
import tqdm
from phasegen.generators import EventGeneratorRandomized


class AnalysisBuilder(object):
    def __init__(self, cfile="config/angle-analysis.json"):
        super(AnalysisBuilder, self).__init__()
        with open(cfile) as f:
            self.conf = json.load(f)
        self.n_events = self.conf["n_events"]
        self.generator = self.conf["generator"]

        # Setup the momentum generation function
        momentum = self.conf["momentum_distribution"]
        function = ROOT.TF1('fPt', *momentum["function"])
        function.SetParameters(*momentum["parameters"])
        self.generator["function"] = function

    def create_generator(self):
        return EventGeneratorRandomized(**self.generator)


class Analysis(object):
    def __init__(self, config=AnalysisBuilder()):
        super(Analysis, self).__init__()
        self.n_events = config.n_events
        self.generator = config.create_generator()

    def transform(self, selections):
        for _ in tqdm.trange(self.n_events):
            particles = self.generator.event()
            for selection in selections:
                selection.transform(particles)
