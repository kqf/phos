from contextlib import contextmanager

import json
import ROOT
import tqdm
from phasegen.generators import EventGeneratorRandomized, EventGenerator


@contextmanager
def root_file(ofile):
    ofile = ROOT.TFile(ofile, "recreate")
    try:
        yield ofile
    finally:
        ofile.Close()


class AnalysisBuilder(object):
    _generators = {
        "normal": EventGenerator,
        "randomized": EventGeneratorRandomized,
    }

    def __init__(self, cfile="config/angle-analysis.json"):
        super(AnalysisBuilder, self).__init__()
        with open(cfile) as f:
            self.conf = json.load(f)
        self.n_events = self.conf["n_events"]
        self.generator = self.conf["generator"]
        self.generator_type = self.conf["generator_type"]

        # Setup the momentum generation function
        momentum = self.conf["momentum_distribution"]
        function = ROOT.TF1('fPt', *momentum["function"])
        function.SetParameters(*momentum["parameters"])
        self.generator["function"] = function

    def create_generator(self):
        build_generator = self._generators.get(self.generator_type, None)
        return build_generator(**self.generator)


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
        return selections
