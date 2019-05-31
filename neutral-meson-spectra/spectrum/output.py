from __future__ import print_function

import ROOT
import tqdm
from contextlib import contextmanager

import sutils as su
from comparator import Comparator
from flatten_dict import flatten
from ptplotter import MulipleOutput
from vis import Visualizer, MultipleVisualizer

# TODO: Introduce more log items for compare etc.
#


def save_item(ofile, name, obj, stop=False):
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

            if stop:
                Comparator(labels=labels, stop=False).compare(hists)
        return

    if obj.__class__.__bases__[0] == tuple:
        for hist in obj:
            hist.Write()
        return

    print("Don't know how to handle", obj, type(obj))


class AnalysisOutput(dict):
    def __init__(self, label, particle="", *args, **kwargs):
        super(AnalysisOutput, self).__init__(*args, **kwargs)
        self.label = label.replace("#", "")
        self.particle = particle

    def plot(self, stop=False):
        with su.rfile(self._ofile(), mode="recreate") as ofile:
            flat = flatten(self, reducer="path")
            for k, v in tqdm.tqdm(flat.iteritems()):
                save_item(ofile, k, v, stop=stop)

    def _ofile(self):
        name = self.label.lower().replace(" ", "-")
        return "results/{}.root".format(name)

    def __repr__(self):
        normal = super(AnalysisOutput, self).__repr__()
        message = 'AnalysisOutput(label="{}", particle="{}"): {}'
        return message.format(self.label, self.particle, normal)


@contextmanager
def open_loggs(name, stop=False, plot=True):
    loggs = AnalysisOutput(name)
    try:
        yield loggs
    finally:
        if not plot:
            return
        loggs.plot(stop=stop)
