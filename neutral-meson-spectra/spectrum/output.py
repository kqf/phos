from comparator import Comparator
from ptplotter import PtPlotter
import ROOT

class LogItem(object):
    def __init__(self, name, histograms, multirange=False):
        super(LogItem, self).__init__()
        self.name = name
        self.histograms = histograms
        self.multirange = multirange
        # print "Created log item", name
        
    def __repr__(self):
        return "LogItem({0}, {1}, {2})".format(
            self.name,
            self.histograms,
            self.multirange
        )   


class AnalysisOutput(object):
    def __init__(self, label, particle="#pi^{0}"):
        super(AnalysisOutput, self).__init__()
        self.particle = particle
        self.label = label
        self.pool = []
        # print "Created analysis output", label
    


    def update(self, stepname, histograms, multirange=False):
        self.pool.append(
            LogItem(stepname, histograms, multirange)
        )

    def plot(self, stop=False):
        for item in self.pool:
            if item == []:
                continue

            try:
                # print 'Drawing', item.name
                if item.multirange:
                    PtPlotter(
                        item.histograms, 
                        self.label, 
                        self.particle
                    ).draw(stop, "{0}/{1}".format(self.label, item.name))
                    continue
            except Exception as e:
                print e, self.pool

        for hist in item.histograms:
                diff = Comparator(
                    stop=stop, 
                    oname="{0}/{1}/{2}-{3}".format(self.label, item.name, hist.GetName(), self.particle)
                )
                diff.compare(hist)

    def append(self, other):
        if not other.pool:
            return

        for item in other.pool:
            if item == []:
                print other.label, other.pool
                continue
            # print item
            item.name = "{0}/{1}".format(other.label, item.name)

        self.pool.extend(filter(lambda x: x != [], other.pool))