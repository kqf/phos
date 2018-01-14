import ROOT
from broot import BROOT as br
import sutils as su
import collections



class SpectrumExtractor(object):

    def handle_empty_fit(f):
        def wrapper(self, mass):
            if not mass.fitted():
                return (0, 0)
            return f(self, mass)
        return wrapper

    def __init__(self, order = []):
        super(SpectrumExtractor, self).__init__()
        rules = {
            'mass': self.mass,
            'width': self.width,
            'spectrum': self.nraw,
            'chi2': self.chi2,
            'npi0': self.npi0,
            'cball_alpha': self.cball_alpha,
            'cball_n': self.cball_n
        }
        self.quantities = [rules[q] for q in order]

    def parameter(self, mass, parname):
        position = mass.sigf.GetParNumber(parname)
        par = mass.sigf.GetParameter(position)
        par_error = mass.sigf.GetParError(position)
        return par, par_error

    @handle_empty_fit
    def mass(self, mass):
        return self.parameter(mass, "M")

    @handle_empty_fit
    def width(self, mass):
        return self.parameter(mass, "#sigma")

    @handle_empty_fit
    def cball_alpha(self, mass):
        return self.parameter(mass, "#alpha")

    @handle_empty_fit
    def cball_n(self, mass):
        return self.parameter(mass, "n")

    @handle_empty_fit
    def npi0(self, mass):
        return mass.number_of_mesons()

    @handle_empty_fit
    def nraw(self, mass):
        npi0 = mass.number_of_mesons()
        return map(lambda x: x / (2. * ROOT.TMath.Pi()), npi0)

    @handle_empty_fit
    def chi2(self, mass):
        ndf = mass.sigf.GetNDF() 
        ndf = ndf if ndf > 0 else 1
        return (mass.sigf.GetChisquare() / ndf, 0) 

    def eval(self, mass):
        mass.extract_data() 
        return [f(mass) for f in self.quantities]


class OutputCreator(object):
    def __init__(self, name, title, label, priority = 999):
        super(OutputCreator, self).__init__()
        self.title = title
        self.label = label
        self.name = name + '_' + filter(str.isalnum, self.label)
        self.priority = priority

    def get_hist(self, bins, data):
        from array import array
        hist = ROOT.TH1F(self.name, self.title, len(bins) - 1, array('d', bins))

        if not hist.GetSumw2N(): 
            hist.Sumw2()

        hist.label = self.label
        hist.priority = self.priority

        for i, (d, e) in enumerate(data):
            hist.SetBinContent(i + 1, d)
            hist.SetBinError(i + 1, e)
        return hist

    @staticmethod
    def output_histogram(name, title, label, priority, bins, data):
        output = OutputCreator(name, title, label, priority)
        return output.get_hist(bins, data)





class RangeTransformer(object):

    _output = 'mass', 'width'
    def __init__(self, options, ptedges, label):
        super(RangeTransformer, self).__init__()
        self.opt = options
        self.ptedges  = ptedges
        self.label = label
        # The fit result
        self.output = None

    def transform(self, masses):
        ExtractorOutput = collections.namedtuple('SpectrumAnalysisOutput', self._output)
        extractor = SpectrumExtractor(self._output)
        values = map(extractor.eval, masses)

        iter_collection = zip(
            self._output, # Ensure ordering of `data`
            zip(*values)
        )
        # Extract the data
        output = {quant: 
            OutputCreator.output_histogram(
                quant,
                quant,
                quant,
                999,
                self.ptedges,
                d
            ) for quant, d in iter_collection
        }

        self.output = ExtractorOutput(**output) 
        ranges = self._fit_ranges(self.output)

        for mass, region in zip(masses, ranges):
            mass.integration_region = region

        return masses

    def _fit_quantity(self, quant, func, par, names, pref):
        fitquant = ROOT.TF1("fitquant" + pref, func)
        fitquant.SetLineColor(46)


        if not self.opt.dead:
            canvas = su.gcanvas(1./ 2., 1, True)
            su.adjust_canvas(canvas)
            su.ticks(canvas) 
            quant.Draw()

        fitquant.SetParameters(*par)
        fitquant.SetParNames(*names)

        # Doesn't fit and use default parameters for 
        # width/mass, therefore this will give correct estimation
        if not self.opt.fit_mass_width:
            [fitquant.FixParameter(i, p) for i, p in enumerate(par)]


        # print self.opt.fit_range
        quant.Fit(fitquant, "q", "", *self.opt.fit_range)

        # print [fitquant.GetParameter(i) for i, p in enumerate(par)]
        quant.SetLineColor(37)
        su.wait(pref + "-paramerisation-" + self.label, self.opt.show_img, True)
        return fitquant

    def _fit_ranges(self, quantities):
        ROOT.gStyle.SetOptStat('')
        mass, sigma = quantities.mass, quantities.width

        massf = self.fit_mass(mass)
        sigmaf = self.fit_sigma(sigma)

        mass_range = lambda pt: (massf.Eval(pt) - self.opt.nsigmas * sigmaf.Eval(pt),
                                 massf.Eval(pt) + self.opt.nsigmas * sigmaf.Eval(pt))

        pt_values = [mass.GetBinCenter(i + 1) for i in range(mass.GetNbinsX())]
        return map(mass_range, pt_values) 
        

    def fit_mass(self, mass):
        return self._fit_quantity(mass,
            self.opt.mass_func,
            self.opt.mass_pars,
            self.opt.mass_names,
            'mass'
        ) 

    def fit_sigma(self, sigma):
        return self._fit_quantity(sigma, 
            self.opt.width_func, 
            self.opt.width_pars, 
            self.opt.width_names, 
            'width'
        )


