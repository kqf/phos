import ROOT
import sutils as su
from comparator import Comparator
from flatten_dict import flatten
from ptplotter import MultiplePlotter, MulipleOutput
from vis import Visualizer


# TODO: Introduce more log items for compare etc
#


class LogItem(object):
    def __init__(self, name, data, mergable=False):
        super(LogItem, self).__init__()
        self.name = name
        self.data = data
        self.mergable = mergable

    def __repr__(self):
        return "LogItem({0}, {1}, {2})".format(
            self.name,
            self.data,
            self.mergable
        )

    def save(self, stop):
        if isinstance(self.data, ROOT.TCanvas):
            oname = "{0}/{1}".format(self.name, self.oname(self.data))
            su.save_canvas_root(self.data, "results/", oname)
            return

        for hist in self.data:
            oname = "{0}/{1}".format(self.name, self.oname(hist))
            diff = Comparator(stop=stop, oname=oname)
            diff.compare(hist)

    def oname(self, hist):
        try:
            return hist.GetName()
        except AttributeError:
            try:
                return hist[0].GetName()
            except BaseException:
                return self.name.split('/')[-1]


class MultirangeLogItem(LogItem):

    def save(self, stop):
        plotter = MultiplePlotter(self.name)
        plotter.transform(self.data, stop)


class MergedLogItem(object):
    def __init__(self, name, loggs, mergable=False):
        super(MergedLogItem, self).__init__()
        self.name = name
        self.loggs = zip(*[logg.data for logg in loggs])
        self.mergable = mergable

    def __repr__(self):
        return "LogItem({0}, {1}, {2})".format(
            self.name,
            self.loggs,
            self.mergable
        )

    def save(self, stop):
        for logg in self.loggs:
            try:
                name = logg[0].GetName()
            except AttributeError:
                name = logg[0][0].GetName()
            output = "{0}/{1}".format(self.name, name)
            diff = Comparator(
                stop=stop,
                oname=output
            )
            diff.compare(logg)


def save_item(ofile, name, obj):
    ofile.mkdir(name)
    ofile.cd(name)

    if type(obj) in {ROOT.TCanvas, ROOT.TH1F, ROOT.TH1D,
                     MulipleOutput, Visualizer}:
        obj.Write()
        return

    if type(obj) == list:
        if obj and type(obj[0]) == tuple:
            labels, hists = zip(*obj)
            if type(hists[0]) not in {ROOT.TH1F, ROOT.TH1D}:
                return
            labels = Comparator(labels=labels, stop=False).compare(hists)
        return
    print obj, type(obj)


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
