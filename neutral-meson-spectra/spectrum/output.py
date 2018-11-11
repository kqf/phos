import ROOT
from comparator import Comparator
from flatten_dict import flatten
from ptplotter import MulipleOutput
from vis import Visualizer, MultipleVisualizer


# TODO: Introduce more log items for compare etc
#


def save_item(ofile, name, obj):
    ofile.mkdir(name)
    ofile.cd(name)

    if type(obj) in {ROOT.TCanvas, ROOT.TH1F, ROOT.TH1D,
                     MulipleOutput, Visualizer, MultipleVisualizer}:
        obj.Write()
        return

    if type(obj) == list:
        if obj and type(obj[0]) == tuple:
            labels, hists = zip(*obj)
            if type(hists[0]) not in {ROOT.TH1F, ROOT.TH1D}:
                return
            labels = Comparator(labels=labels, stop=False).compare(hists)
        return
    print "Don't know how to handle", obj, type(obj)


class AnalysisOutput(dict):
    def __init__(self, label, particle="", *args, **kwargs):
        super(AnalysisOutput, self).__init__(*args, **kwargs)
        self.label = label
        self.particle = particle

    def plot(self, stop=False):
        print
        ofile = ROOT.TFile(self._ofile(), "recreate")
        flattened = flatten(self, reducer="path")
        for k, v in flattened.iteritems():
            save_item(ofile, k, v)
        ofile.Write()

    def _ofile(self):
        name = self.label.lower().replace(" ", "-")
        return "results/{}.root".format(name)

    def __repr__(self):
        normal = super(AnalysisOutput, self).__repr__()
        message = 'AnalysisOutput(label="{}", particle="{}"): {}'
        return message.format(self.label, self.particle, normal)
