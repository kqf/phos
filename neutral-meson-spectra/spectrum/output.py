from comparator import Comparator
from ptplotter import PtPlotter
import ROOT

# TODO: Introduce more log items for compare etc
# 
class LogItem(object):
    def __init__(self, name, data, mergable=False):
        super(LogItem, self).__init__()
        self.name = name
        self.data = data
        self.mergable = mergable
        # print "Created log item", name
        
    def __repr__(self):
        return "LogItem({0}, {1}, {2})".format(
            self.name,
            self.data,
            self.mergable
        )   

    def save(self, particle, stop):
        for hist in self.data:
            diff = Comparator(
                stop=stop, 
                oname="{0}/{1}-{2}".format(self.name, hist.GetName(), particle)
            )
            diff.compare(hist)


class MultirangeLogItem(LogItem):

    def save(self, particle, stop):
        plotter = PtPlotter(
            self.data, 
            self.name, 
            particle
        )
        plotter.draw(stop, self.name)


class MergedLogItem(object):
    def __init__(self, name, loggs):
        super(MergedLogItem, self).__init__()
        self.name = name
        self.loggs = zip(*[logg.data for logg in loggs])
        
    def __repr__(self):
        return "LogItem({0}, {1}, {2})".format(
            self.name,
            self.loggs,
            self.mergable
        )   

    def save(self, particle, stop):
        for logg in self.loggs:
            try:
                name = logg[0].GetName()
            except AttributeError:
                name = logg[0][0].GetName()

            diff = Comparator(
                stop=stop, 
                oname="{0}/{1}-{2}".format(self.name, name, particle)
            )
            diff.compare(logg)


class AnalysisOutput(object):
    def __init__(self, label, particle="#pi^{0}"):
        super(AnalysisOutput, self).__init__()
        self.particle = particle
        self.label = label
        self.pool = []
    
    def update(self, stepname, histograms, multirange=False, mergable=False):
        logtype = MultirangeLogItem if multirange else LogItem

        self.pool.append(
            logtype("{0}/{1}".format(self.label, stepname), histograms, mergable)
        )

    def plot(self, stop=False):
        for item in self.pool:
            item.save(self.particle, stop)

    def append(self, other):
        if not other.pool:
            return

        for item in other.pool:
            if item == []:
                print other.label, other.pool
                continue
            # print item
            item.name = "{0}/{1}".format(self.label, item.name)

        self.pool.extend(filter(lambda x: x != [], other.pool))


    def mergelist(self):
        return [item for item in self.pool if item.mergable]