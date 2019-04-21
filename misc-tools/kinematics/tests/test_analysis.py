import ROOT

from phasegen.analysis import Analysis


class SimpleAnalysis(object):
    def __init__(self, ofile="output.root"):
        super(SimpleAnalysis, self).__init__()
        self.hist = ROOT.TH1F("hMomentum", "test", 10, 0, 3)
        self.ofile = ofile

    def transform(self, particles):
        _, original = particles
        self.hist.Fill(original.P())

    def write(self):
        ofile = ROOT.TFile(self.ofile, "recreate")
        self.hist.Write()
        ofile.Close()


def test_analysis(config):
    selections = Analysis().transform([
        SimpleAnalysis()
    ])

    for selection in selections:
        selection.write()
