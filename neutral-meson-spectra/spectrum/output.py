import ROOT
from comparator import Comparator
from ptplotter import MultiplePlotter
import sutils as su
from flatten_dict import flatten

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


class AnalysisOutput(dict):
    def __init__(self, label, particle="", *args, **kwargs):
        super(AnalysisOutput, self).__init__(*args, **kwargs)
        self.label = label
        self.particle = particle

    def plot(self, stop=False):
        print flatten(self, reducer="path")

    def __repr__(self):
        normal = super(AnalysisOutput, self).__repr__()
        message = 'AnalysisOutput(label="{}", particle="{}"): {}'
        return message.format(self.label, self.particle, normal)
