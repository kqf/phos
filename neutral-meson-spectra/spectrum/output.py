from comparator import Comparator
from ptplotter import MultiplePlotter
# import ROOT

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
        for hist in self.data:
            diff = Comparator(
                stop=stop,
                oname="{0}/{1}".format(self.name, self.oname(hist)),
                rrange=(0, 2),
            )
            diff.compare(hist)

    def oname(self, hist):
        try:
            return hist.GetName()
        except AttributeError:
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

            diff = Comparator(
                stop=stop,
                oname="{0}/{1}".format(self.name, name),
                rrange=(0, 2),
            )
            diff.compare(logg)


class AnalysisOutput(object):
    def __init__(self, label, particle=""):
        super(AnalysisOutput, self).__init__()
        self.label = label
        self.pool = []
        # if particle:
        # self.label = "{0}-{1}".format(self.label, particle)

    def update(self, stepname, histograms, multirange=False, mergable=False):
        logtype = MultirangeLogItem if multirange else LogItem

        self.pool.insert(
            0,
            logtype("{0}/{1}".format(
                self.label,
                stepname), histograms, mergable)
        )

    def plot(self, stop=False):
        # default = ROOT.gROOT.IsBatch()
        # ROOT.gROOT.SetBatch(not stop)
        for item in self.pool:
            item.save(stop)
        # ROOT.gROOT.SetBatch(default)

    def append(self, other):
        if not other.pool:
            return

        for item in other.pool:
            if item == []:
                continue
            item.name = "{0}/{1}".format(self.label, item.name)

        self.pool.extend(filter(lambda x: x != [], other.pool))

    def mergelist(self):
        return [item for item in self.pool if item.mergable]
