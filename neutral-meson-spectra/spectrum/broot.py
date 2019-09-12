import ROOT
import array
import copy
import os
from collections import namedtuple
import six

import numpy as np
import tqdm
from repoze.lru import lru_cache
from six.moves import urllib

ROOT.TH1.AddDirectory(False)


class BROOT(object):
    class prop(object):
        _properties = {'label': '',
                       'logy': 0,
                       'logx': 0,
                       'priority': 999,
                       'marker': 0}

        def __init__(self, label='', logy=0, logx=0, priority=999, marker=0):
            super(BROOT.prop, self).__init__()
            self.__dict__.update(self._properties)
            # Add self.set_properties
            self.marker = marker
            self.label = label
            self.logy = logy
            self.logx = logx
            self.priority = priority
            # self.fitfunc = fitfunc

        def set_properties(self, source, force=False):
            assert self.has_properties(source),\
                "There is no properties in source histogram"
            self.copy(self, source, force)

        @classmethod
        def same_as(klass, a, b):
            assert klass.has_properties(b), \
                "There is no properties in b histogram"
            return all(a.__dict__[prop] == b.__dict__[prop]
                       for prop in klass._properties)

        @classmethod
        def init(klass, hist, force=True):
            self = klass()
            klass.copy(hist, self, force)

        @classmethod
        def copy(klass, dest, source, force=False):
            if not klass.has_properties(source):
                klass.init(dest)

            keys = (key for key in klass._properties
                    if key not in dir(dest) or force)
            for key in keys:
                dest.__dict__[key] = copy.deepcopy(source.__dict__[key])

        @staticmethod
        def copy_everything(dest, source):
            keys = (key for key in dir(source) if key not in dir(dest))
            for key in keys:
                dest.__dict__[key] = source.__dict__[key]

        @classmethod
        def has_properties(klass, hist):
            return all(prop in dir(hist) for prop in klass._properties)

    class io(object):
        def __init__(self):
            super(BROOT.io, self).__init__()

        @classmethod
        def _read_file(klass, filename, directory='input-data/'):
            if os.path.isfile(filename):
                return ROOT.TFile(filename)

            if directory not in filename:
                return klass._read_file(directory + filename, directory)

            if '.root' not in filename:
                return klass._read_file(filename + '.root', directory)

            raise IOError('No such file: {0}'.format(filename))

        @classmethod
        def _dir_to_list(klass, tdir):
            try:
                keys = tdir.GetListOfKeys()
            except AttributeError:  # It's not a tdirectory
                return tdir

            nlist = ROOT.TList()
            # nlist.SetOwner(True)
            for key in keys:
                nlist.Add(key.ReadObj().Clone())
            return nlist

        @classmethod
        def _read_list(klass, filename, selection):
            infile = klass._read_file(filename)

            if not selection:
                return klass._dir_to_list(infile)

            lst = infile.Get(selection)

            if not lst:
                infile.ls()
                raise IOError('No such selection {1} in file: \
                    {0}'.format(filename, selection))

            return klass._dir_to_list(lst)

        @classmethod
        @lru_cache(maxsize=None)
        def read(klass, filename, selection, histname):
            lst = klass._read_list(filename, selection)
            hist = lst.FindObject(histname)

            if not hist:
                raise IOError(
                    'No such histogram {2} for selection {1} in file: {0}'
                    .format(filename, selection, histname))

            hist = hist.Clone()
            BROOT.prop.init(hist)
            lst.IsA().Destructor(lst)
            return hist

        # NB: Keep this function to keep memory/time performance
        @classmethod
        def read_multiple(klass, filename, selection, histnames):
            lst = klass._read_list(filename, selection)

            histograms = []
            iternames = histnames
            if len(histnames) > 10:
                iternames = tqdm.tqdm(histnames)
            for histname in iternames:
                if not histname:
                    histograms.append(None)
                    continue

                hist = lst.FindObject(histname)
                if not hist:
                    raise IOError(
                        'No such histogram {2} for selection {1} in file: {0}'
                        .format(filename, selection, histname))

                hist = hist.Clone()
                BROOT.prop.init(hist)
                histograms.append(hist)
            lst.IsA().Destructor(lst)
            return histograms

        @classmethod
        def save(klass, obj, fname='output.root',
                 selection='', option='recreate'):
            ofile = ROOT.TFile(fname, option)

            if not selection:
                obj.Write()
                ofile.Close()

            olist = ROOT.TList()
            olist.SetOwner(True)
            cloned = BROOT.clone(obj, '')
            olist.Add(cloned)
            olist.Write(selection, 1)
            ofile.Close()

        @classmethod
        def read_from_canvas(self, canvas):
            stack = canvas.FindObject("mainpad").FindObject("test")
            return stack.GetHists()

        @classmethod
        def hepdata(klass, record, ofilename, table="Table 1"):

            link = 'https://www.hepdata.net/download/table/{}/{}/1/root'
            try:
                download = link
                url = download.format(record, table.replace(" ", ""))
                response = urllib.request.urlopen(url)

                with open(ofilename, 'wb') as f:
                    f.write(response.read())
            except urllib.error.HTTPError as e:
                raise IOError('HTTP error {0}\nInvalid record {1}\n{2}'
                              .format(e.code, record, download.format(record)))

            except urllib.error.URLError as e:
                raise IOError('URL error {0}\nInvalid record {1}\n{2}'
                              .format(e.code, record, download.format(record)))

    def __init__(self):
        super(BROOT, self).__init__()

    @classmethod
    def BH(klass, THnT, *args, **kwargs):
        hist = THnT(*args)
        klass.setp(hist, klass.prop(**kwargs))
        return hist

    @classmethod
    def setp(klass, dest, source=None, force=False):
        if not source:
            source = klass.prop()
        klass.prop.copy(dest, source, force)

    @classmethod
    def clone(klass, hist, name='_copied', replace=False):
        name = name if replace else hist.GetName() + name
        cloned = hist.Clone(name)
        prop = hist if klass.prop.has_properties(hist) else klass.prop()
        klass.setp(cloned, prop)
        return cloned

    @classmethod
    def copy(klass, hist, name='_copied', replace=False):
        hist = BROOT.clone(hist, name, replace)
        hist.Reset()
        return hist

    @classmethod
    def projection(klass, hist, name, a, b, axis='x'):
        axis, name = axis.lower(), hist.GetName() + name

        if '%d_%d' in name:
            name = name % (a, b)

        # NB:  By default ProjectionX takes the last bin as well.
        #      We don't want to take last bin as it contains the
        #      beginning of the next bin. Therefore use "b - 1" here!
        #

        args = name, a, b - 1
        proj = hist.ProjectionX(
            *args) if axis == 'x' else hist.ProjectionY(*args)
        klass.setp(proj, hist, force=True)
        return proj

    @classmethod
    def project_range(klass, hist, name, xa, xb, axis='x'):
        bin = klass.bincenterf(hist, 'x' not in axis)
        return klass.projection(hist, name, bin(xa), bin(xb), axis)

    @classmethod
    def same(klass, hist1, hist2):
        if klass.prop.has_properties(hist1):
            return klass.prop.same_as(hist2, hist1)

        if klass.prop.has_properties(hist2):
            return klass.prop.same_as(hist1, hist2)

        raise AttributeError(
            'Neither of hist1 and hist2 have BROOT properties')

    @classmethod
    def ratio(klass, a, b, option="B", loggs=None):
        ratio = a.Clone('ratio' + a.GetName())
        klass.prop.copy_everything(ratio, a)

        # if ratio.GetNbinsX() != b.GetNbinsX():
        # ratio, b = klass.rebin_as(ratio, b)
        if type(b) == ROOT.TF1:
            ratio.Divide(b)
        else:
            ratio.Divide(a, b, 1, 1, option)

        try:
            label = a.label + ' / ' + b.label
        except AttributeError:
            label = ""

        # at, bt = a.GetYaxis().GetTitle(), b.GetYaxis().GetTitle()
        # ratio.GetYaxis().SetTitle(at + '/' + bt)
        ratio.GetYaxis().SetTitle(label)

        title = a.GetTitle() + ' / ' + b.GetTitle()
        ratio.SetTitle(title)

        if not ratio.GetSumw2N():
            ratio.Sumw2()

        return ratio

    @classmethod
    def set_nevents(klass, hist, nevents, norm=False):
        hist.nevents = nevents
        if norm:
            hist.Scale(1. / nevents)

    @classmethod
    def rebin_as(klass, hist1, hist2):
        if type(hist2) == ROOT.TF1:
            return hist1, hist2

        if hist1.GetNbinsX() == hist2.GetNbinsY():
            return hist1, hist2

        def nbins(x):
            return x.GetNbinsX()

        a, b = (hist1, hist2) if nbins(
            hist1) > nbins(hist2) else (hist2, hist1)
        rebinned = klass.rebin_proba(a, klass.edges(b))
        return (rebinned, b) if a == hist1 else (b, rebinned)

    @classmethod
    def rebin_proba(klass, hist, edges, name="_rebinned"):
        edges = array.array('d', edges)
        rebin = hist.Rebin(len(edges) - 1, hist.GetName() + name, edges)

        if not rebin.GetSumw2N():
            rebin.Sumw2()

        for i in range(1, len(edges)):
            delta = edges[i] - edges[i - 1]
            rebin.SetBinContent(i, rebin.GetBinContent(i) / delta)

        if klass.prop.has_properties(hist):
            klass.setp(rebin, hist, force=True)
        return rebin

    @classmethod
    def sum(klass, histograms, label=None):
        if not histograms:
            raise ValueError("You are trying to sum 0 histograms")

        first = histograms[0]
        label = label if label else first.label

        result = klass.copy(first, label)
        klass.setp(result, first)
        result.label = label

        # Finally sum the histograms
        for h in histograms:
            result.Add(h)

        return result

    @classmethod
    def scalew(klass, hist, factor=None):
        if type(hist) == ROOT.TF1:
            return

        if factor is None:
            factor = min(hist.GetBinWidth(i)
                         for i in klass.range(hist))
        hist.Scale(factor, "width")
        return hist

    @classmethod
    def scalewidth(klass, hist):
        if not hist.GetSumw2N():
            hist.Sumw2()

        for i in klass.range(hist):
            width = hist.GetBinWidth(i)
            hist.SetBinContent(i, hist.GetBinContent(i) / width)
        return hist

    @staticmethod
    def bincenterf(hist, isxaxis=True):
        axis = hist.GetXaxis() if isxaxis else hist.GetYaxis()
        return lambda x: axis.FindBin(x)

    @classmethod
    def area_and_error(klass, hist, a, b):
        if a == b:
            return 0, 0
        area, areae = ROOT.Double(), ROOT.Double()
        bin = klass.bincenterf(hist)
        area = hist.IntegralAndError(bin(a), bin(b), areae)
        return area, areae

    @classmethod
    def init_inputs(klass, func):
        def f(self, hists, *args, **kwargs):
            for h in hists:
                if not h:
                    continue
                klass.setp(h)
            return func(self, hists, *args, **kwargs)
        return f

    @staticmethod
    def define_colors():
        rcolors = [
            ROOT.kRed + 1,
            ROOT.kBlue - 3,
            ROOT.kGreen + 1,
            ROOT.kYellow + 1,
            ROOT.kOrange + 1,
            ROOT.kBlack + 1,
        ]
        return rcolors

    @classmethod
    def bins(klass, hist):
        contents = np.array([hist.GetBinContent(i) for i in klass.range(hist)])
        errors = np.array([hist.GetBinError(i) for i in klass.range(hist)])
        centers = np.array([hist.GetBinCenter(i) for i in klass.range(hist)])
        HistMatrix = namedtuple(
            'HistMatrix', ['contents', 'errors', 'centers'])
        return HistMatrix(contents, errors, centers)

    @classmethod
    def hist2dict(klass, hist):
        binsdict = klass.bins(hist)._asdict()
        return {k: list(v) for k, v in six.iteritems(binsdict)}

    @classmethod
    def systematic_deviation(klass, histograms):
        matrix = np.array([klass.bins(h)[0] for h in histograms])

        rms, mean = np.std(matrix, axis=0), np.mean(matrix, axis=0)

        klass.setp(histograms[0])
        syst = klass.copy(histograms[0], 'RMS/mean')
        syst.GetYaxis().SetTitle('rms/mean')
        syst.label = 'yield extraction'

        for i, r in enumerate(rms / mean):
            syst.SetBinContent(i + 1, r)

        return syst, rms, mean

    @classmethod
    def range(klass, hist, axis='x', start=1, edges=False):
        nbins = hist.GetNbinsX() if 'x' in axis.lower() else hist.GetNbinsY()
        # NB: Default value should be 1
        #     one should use 0 if bin edges are needed
        return range(start, nbins + 1 + int(edges))

    @classmethod
    def pars(klass, tfunc, npars=None):
        if not npars:
            npars = tfunc.GetNpar()

        pp = [tfunc.GetParameter(i) for i in range(npars)]
        ep = [tfunc.GetParError(i) for i in range(npars)]

        FitPars = namedtuple('FitPars', ['pars', 'errors'])
        return FitPars(pp, ep)

    @classmethod
    def empty_bins(klass, hist, tolerance=1e-10):
        return [i for i in klass.range(hist)
                if hist.GetBinContent(i) < tolerance]

    @classmethod
    def diff(klass, hist1, hist2, tol=1e-10):
        bins1, errors1, centers = klass.bins(hist1)
        bins2, errors2, centers = klass.bins(hist2)

        def kernel(x, y):
            return abs(x - y) < tol

        bins_ok = map(kernel, bins1, bins2)
        errors_ok = map(kernel, errors1, errors2)
        return all(bins_ok) and all(errors_ok)

    @classmethod
    def set_to_zero(klass, hist, rrange):
        a, bb = rrange

        # NB: It should be reversed indicating that we want to
        #     keep have clean interface for spmc: weight, (0, 1) - range
        #

        bins = list(b for b in klass.range(hist)
                    if not (a < hist.GetBinCenter(b) < bb))
        # NB: Don't include the last bin,
        #     othervise we will count twice the same point
        #     in BROOT.sum_trimm method

        # TODO: Check this!?
        for bin in bins:
            hist.SetBinContent(bin, 0)
            hist.SetBinError(bin, 0)

    @classmethod
    def sum_trimm(klass, hists, ranges):
        clones = list(map(klass.clone, hists))
        for c, r in zip(clones, ranges):
            klass.set_to_zero(c, r)

        return klass.sum(clones)

    @classmethod
    def confidence_intervals(klass, hist, func, options="R", histbining=None):
        ci = klass.copy(histbining or hist)
        hist.Fit(func, options)
        ROOT.TVirtualFitter.GetFitter().GetConfidenceIntervals(ci)
        ci.SetStats(False)
        ci.SetOption("E3")
        ci.SetFillColor(3)
        return ci

    @classmethod
    def function2histogram(klass, func, hist):
        newhist = klass.copy(hist)
        for b in klass.range(hist):
            newhist.SetBinContent(
                b,
                func.Eval(hist.GetBinCenter(b))
            )
        return newhist

    @classmethod
    def chi2(klass, hist1, hist2, rrange=None):
        assert hist1.GetNbinsX() == hist2.GetNbinsX(), \
            "Histograms should have the same binning"
        difference = klass.copy(hist1, 'difference')
        difference.Add(hist2, hist1, -1)

        def within_range(x):
            if not rrange:
                return True
            a, b = rrange
            return a < x < b

        chi2 = [
            (b / err) ** 2
            for b, err, center in zip(*klass.bins(difference))
            if within_range(center)
        ]
        chi2 = sum(chi2)
        return chi2

    @classmethod
    def chi2ndf(klass, hist1, hist2):
        assert hist1.GetNbinsX() > 0, \
            "Histograms should have more than 0 bins"

        return klass.chi2(hist1, hist2) / hist1.GetNbinsX()

    @classmethod
    def hist_range(klass, hist):
        x = hist.GetXaxis()
        return (
            hist.GetBinCenter(x.GetFirst()),
            hist.GetBinCenter(x.GetLast())
        )

    @classmethod
    def vec_to_bins(klass, data):
        nbins = len(data)
        step = (max(data) - min(data)) / nbins
        return nbins, min(data) - 0.5 * step, max(data) + 0.5 * step

    @classmethod
    def average(klass, histograms, label=None):
        summed = klass.sum(histograms, label)
        summed.Scale(1. / len(histograms))
        return summed

    @classmethod
    def chi2errors(klass, histogram, scale=1):
        functions = histogram.GetListOfFunctions()
        if functions.GetSize() == 0:
            raise ValueError("Histogram should be fitted")

        function = functions.At(0)
        for i in klass.range(histogram):
            x = histogram.GetBinCenter(i)
            value = histogram.GetBinContent(i)
            sigma = histogram.GetBinError(i)
            chi2 = ((value - function.Eval(x)) / sigma) ** 2
            histogram.SetBinError(i, chi2 * scale)
        return histogram

    @classmethod
    def hist2array(klass, hist):
        data = klass.bins(hist)
        return data.contents

    @classmethod
    def bin_centers(klass, hist):
        centers = klass.copy(hist, "_centers")
        centers.Sumw2()
        for i in klass.range(centers):
            centers.SetBinContent(i, centers.GetBinCenter(i))
        return centers

    @classmethod
    def divide_by_bin_centers(klass, hist):
        centers = klass.bin_centers(hist)
        divided = klass.ratio(hist, centers, option="")
        divided.SetTitle(hist.GetTitle())
        divided.GetXaxis().SetTitle(hist.GetXaxis().GetTitle())
        divided.GetYaxis().SetTitle(hist.GetYaxis().GetTitle())
        return divided

    @classmethod
    def unity(klass, hist):
        ones = klass.copy(hist)
        for i in klass.range(ones):
            ones.SetBinContent(i, 1)
            ones.SetBinError(i, 0)
        return ones

    @classmethod
    def tf1_sum(klass, func1, func2, name="sum"):
        np1, np2 = func1.GetNpar(), func2.GetNpar()
        start, stop = ROOT.Double(), ROOT.Double()
        func1.GetRange(start, stop)

        def summed(x, par):
            par = array.array('d', par)
            return func1.EvalPar(x, par[:np1]) + func2.EvalPar(x, par[np1:])

        return ROOT.TF1(name, summed, start, stop, np1 + np2)

    @classmethod
    def edges(klass, x):
        return [x.GetBinLowEdge(i) for i in klass.range(x, edges=True)]
