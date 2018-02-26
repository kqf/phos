from comparator import Comparator
from broot import BROOT as br


class HistogramSelector(object):

    def __init__(self, histname):
        super(HistogramSelector, self).__init__()
        self.histname = histname

    def transform(self, inputs, loggs):
        output = inputs._asdict()[self.histname]
        return output


class Pipeline(object):

    def __init__(self, steps):
        super(Pipeline, self).__init__()
        self.steps = steps

    def transform(self, inputs, loggs):
        updated = inputs
        for step in self.steps:
            updated = step.transform(updated, loggs)
        return updated


class RatioUnion(object):

    def __init__(self, numerator, denominator, error="B"):
        super(RatioUnion, self).__init__()
        print "ratio", numerator, denominator
        self.numerator = numerator
        self.denominator = denominator

        print self.numerator, self.denominator
        self.error = error

    def transform(self, inputs, loggs):
        numerator = self.numerator.transform(inputs, loggs)
        denominator = self.denominator.transform(inputs, loggs)

        numerator, denominator = br.rebin_as(numerator, denominator)
        br.scalew(denominator)
        br.scalew(numerator)

        diff = Comparator()
        return br.ratio(numerator, denominator, self.error)

