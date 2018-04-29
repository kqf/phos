from spectrum.transformer import TransformerBase
from spectrum.pipeline import Pipeline
from spectrum.input import SingleHistInput
from array import array


class EpSlicer(TransformerBase):

    def __init__(self, options, plot):
        super(EpSlicer, self).__init__(plot)
        self.options = options

    def transform(self, data, loggs):
        output = data.ProjectionY()
        rebinned = output.Rebin(
            len(self.options.ptedges) - 1,
            data.GetName() + "_rebinned",
            array('d', self.options.ptedges)
        )
        return rebinned


class EpRatioEstimator(TransformerBase):

    def __init__(self, options, plot=False):
        super(EpRatioEstimator, self).__init__(plot)
        self.options = options
        self.pipeline = Pipeline([
            ('input', SingleHistInput(options.histname)),
            ('slicer', EpSlicer(options.pt, plot)),

        ])
