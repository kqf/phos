from trigger.utils import trendhist
from random import shuffle


def test_trend_hist(nbins=100):
    bins = range(2000, 2201)
    shuffle(bins)
    print bins
    contents = [b + 1 for b in bins]
    trendhist(bins, contents)
