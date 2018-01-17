#!/usr/bin/python

from invariantmass import invariant_mass_selector

class DataSlicer(object):
    def __init__(self, options, all_options):
        super(DataSlicer, self).__init__()
        self.opt = options
        self.extract = invariant_mass_selector(self.opt.use_mixed, all_options)


    def transform(self, inputs):
        intervals = zip(self.opt.ptedges[:-1], self.opt.ptedges[1:])
        assert len(intervals) == len(self.opt.rebins), \
            'Number of intervals is not equal to the number of rebin parameters'

        common_inputs = lambda x, y: self.extract(inputs, x, y)
        return map(common_inputs,
            intervals,
            self.opt.rebins
        )