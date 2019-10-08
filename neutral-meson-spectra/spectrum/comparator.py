import spectrum.broot as br
from spectrum.vis import VisHub


class Comparator(object):
    def __init__(self, size=(1, 1), rrange=(), crange=(),
                 stop=True, oname='', labels=None, **kwargs):
        super(Comparator, self).__init__()
        self.vi = VisHub(size, rrange, crange, stop, oname, labels, **kwargs)

    def compare(self, *args, **kwargs):
        def contains_objs(x):
            return all('__iter__' not in dir(i) for i in x)

        # Halndle coma separated histograms "obj"
        #
        if contains_objs(args):
            return self.vi.compare_visually(args, **kwargs)

        # Halndle single list of histograms "[obj]"
        #
        if len(args) == 1 and contains_objs(args[0]):
            return self.vi.compare_visually(args[0], **kwargs)

        # Halndle two lists of histograms "[[obj, obj, ...], [obj, obj, ...]]"
        #
        if len(args) == 2 and all(map(contains_objs, args)):
            return self.compare_set_of_histograms(args, **kwargs)

        # Handle sets of histograms "[[obj, obj, obj]]"
        #
        if len(args) == 1 and all(map(contains_objs, args[0])):
            return self.compare_set_of_histograms(args[0], **kwargs)

        message = "Can't deduce what are you" \
            " trying to do with these arguments:\n {}".format(args)
        raise IOError(message)

    def compare_multiple_ratios(self, hists, baselines,
                                comparef=None, **kwargs):
        if not comparef:
            comparef = self.vi.compare_visually
        comparef(list(map(br.ratio, hists, baselines)), **kwargs)

    def compare_ratios(self, hists, baseline,
                       comparef=None, logy=False, **kwargs):
        if not comparef:
            comparef = self.vi.compare_visually

        def ratio(x):
            return br.ratio(x, baseline)
        comparef(list(map(ratio, hists)))

    def compare_set_of_histograms(self, l, comparef=None, **kwargs):
        if not comparef:
            comparef = self.vi.compare_visually

        result = [comparef(hists, **kwargs) for hists in zip(*l)]
        if len(result) > 1:
            return result[0]
        return result
