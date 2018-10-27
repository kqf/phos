import ROOT
from spectrum.analysis import Analysis
from spectrum.pipeline import TransformerBase
from spectrum.pipeline import Pipeline, ParallelPipeline, HistogramSelector
from spectrum.pipeline import ReduceArgumentPipeline
from spectrum.pipeline import HistogramScaler
from spectrum.broot import BROOT as br


class NonlinearityParamExtractor(TransformerBase):

    def __init__(self):
        self.labels = None

    def read_labels(self, data):
        data, mc = data
        output = []
        for d in mc:
            try:
                real, mixing = d.transform()
            except AttributeError:
                # Composite MC
                high, low = d
                real, mixing = low.transform()
            output.append(
                map(float, real.GetTitle().split())
            )
        return output

    def transform(self, data, loggs):
        # Run transform two times:
        # at the very beginning to read the labels and exit
        # and at the end to form the final output
        if not self.labels:
            self.labels = self.read_labels(data)
            return data
        chi2 = data
        assert len(chi2) == len(self.labels), "Wrong number of mc samples"

        a, sigma = zip(*self.labels)
        bins = list(br.vec_to_bins(set(a))) + list(br.vec_to_bins(set(sigma)))
        hist = ROOT.TH2F("nonlinearity_scan",
                         "Chi2/ndf for data and mc; a; #sigma, GeV/c", *bins)
        chi2_params = {}
        for c, b in zip(chi2, self.labels):
            hist.Fill(b[0], b[1], c)
            chi2_params[tuple(b)] = c

        msg = "The most optimal parameters are: {}, chi2 = {}, index = {}"
        optimal = min(chi2_params, key=lambda x: chi2_params[x])
        print msg.format(
            optimal,
            chi2_params[optimal],
            self.labels.index(list(optimal))
        )
        return hist


def chi2_func(hist1, hist2):
    # Comparator().compare(hist1, hist2)
    return br.chi2ndf(hist1, hist2)


class NonlinearityScan(TransformerBase):
    def __init__(self, options, chi2_=br.chi2ndf, plot=True):
        super(NonlinearityScan, self).__init__()
        mass = Pipeline([
            ("reconstruction", Analysis(options.analysis, plot)),
            ("mass", HistogramSelector("mass")),
            ("scale", HistogramScaler(factor=options.factor)),
        ])

        masses_mc = ParallelPipeline([
            ("mass" + str(i), mass)
            for i in range(options.nbins ** 2)
        ])

        mass_estimator_data = Pipeline([
            ("reconstruction", Analysis(options.analysis_data, plot)),
            ("mass", HistogramSelector("mass")),
        ])

        chi2 = ReduceArgumentPipeline(
            masses_mc,
            mass_estimator_data,
            chi2_
        )

        extractor = NonlinearityParamExtractor()
        self.pipeline = Pipeline([
            ("read-titles", extractor),
            ("chi2", chi2),
            ("dump", extractor)
        ])


def form_histnames(nbins=4):
    histnames = sum([
        [
            "hMassPt_{}_{}".format(i, j),
            "hMixMassPt_{}_{}".format(i, j),
        ]
        for j in range(nbins)
        for i in range(nbins)
    ], [])
    return histnames
