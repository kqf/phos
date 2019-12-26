from __future__ import print_function
import ROOT
import pandas as pd

from contextlib import contextmanager

import six
import tqdm
from flatten_dict import flatten

import spectrum.sutils as su

from spectrum.comparator import Comparator
from spectrum.input import Input
from spectrum.ptplotter import MulipleOutput
from spectrum.vis import MultipleVisualizer, Visualizer


def save_tobject(obj):
    if type(obj) not in {ROOT.TCanvas, ROOT.TH1F, ROOT.TH1D,
                         MulipleOutput, Visualizer, MultipleVisualizer}:
        return False

    obj.Write()
    return True


def save_composite(obj, stop, skip_merged):
    if skip_merged:
        return False

    exclude = {MulipleOutput, Visualizer,
               MultipleVisualizer, pd.DataFrame}

    if type(obj) == list or type == tuple:
        if obj and type(obj[0]) == tuple:
            labels, hists = zip(*obj)
            if type(hists[0]) in exclude:
                return True
            try:
                Comparator(labels=labels, stop=stop).compare(hists)
            except (IOError, AttributeError):
                pass
            return True
    return False


def save_iterables(obj):
    container = obj.__class__.__bases__[0] == tuple or type(obj) == tuple
    content = type(obj[0]) not in {Input}
    if container and content:
        for hist in obj:
            hist.Write()
        return True
    return False


def save_item(ofile, name, obj, skip_merged, stop=False):
    ofile.mkdir(name)
    ofile.cd(name)

    if type(obj) == pd.DataFrame:
        return

    if save_tobject(obj):
        return

    if save_composite(obj, stop, skip_merged=skip_merged):
        return

    if save_iterables(obj):
        return

    print("Don't know how to handle", obj, type(obj))


class LogItem(dict):
    def __init__(self, label, *args, **kwargs):
        super(LogItem, self).__init__(*args, **kwargs)
        self.label = label.replace("#", "")

    def save(self, stop=False, skip_merged=False):
        with su.rfile(self._ofile(), mode="recreate") as ofile:
            flat = flatten(self, reducer="path")
            for k, v in tqdm.tqdm(six.iteritems(flat)):
                path = k.replace("output", "")
                save_item(ofile, path, v, skip_merged=skip_merged, stop=stop)

    def _ofile(self):
        name = self.label.lower().replace(" ", "-")
        return "results/{}.root".format(name)

    def __repr__(self):
        normal = super(LogItem, self).__repr__()
        message = 'LogItem(label="{}"): {}'
        return message.format(self.label, normal)


@contextmanager
def open_loggs(name="", stop=False, shallow=False):
    loggs = LogItem(name)
    yield loggs
    if not name:
        return
    loggs.save(stop=stop, skip_merged=shallow)
