import ROOT
import array
import os
from collections import namedtuple
import six

import numpy as np
import tqdm
from contextlib import contextmanager
from repoze.lru import lru_cache
from six.moves import urllib
from copy import deepcopy

ROOT.TH1.AddDirectory(False)

BR_COLORS = [
    ROOT.kRed + 1,
    ROOT.kBlue - 3,
    ROOT.kGreen + 1,
    ROOT.kYellow + 1,
    ROOT.kOrange + 1,
    ROOT.kBlack + 1,
    ROOT.kGray + 1,
    ROOT.kMagenta + 1,
    ROOT.kCyan + 1,
    # ROOT.kSpring + 1,
    ROOT.kTeal + 1,
    ROOT.kAzure + 1,
    ROOT.kViolet + 1,
    ROOT.kPink + 1,
]


class _prop(object):
    _properties = {
        "label": "",
        "logy": 0,
        "logx": 0,
        "priority": 999,
        "marker": 0
    }

    def __init__(self, label="", logy=0, logx=0, priority=999, marker=0):
        super(_prop, self).__init__()
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
            dest.__dict__[key] = deepcopy(source.__dict__[key])

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
        super(io, self).__init__()

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
        with tfile(filename) as infile:
            if not selection:
                return klass._dir_to_list(infile)

            lst = infile.Get(selection)

            if not lst:
                infile.ls()
                print(filename, selection)
                raise IOError("No such selection {1} in file: \
                    {0}".format(filename, selection))
            return klass._dir_to_list(lst)

    @classmethod
    @lru_cache(maxsize=None)
    def read(klass, filename, selection, histname):
        lst = klass._read_list(filename, selection)
        hist = lst.FindObject(histname)

        if not hist:
            raise IOError(
                "No such histogram {2} for selection {1} in file: {0}"
                .format(filename, selection, histname))

        hist = hist.Clone()
        _prop.init(hist)
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
                    "No such histogram {2} for selection {1} in file: {0}"
                    .format(filename, selection, histname))

            hist = hist.Clone()
            _prop.init(hist)
            histograms.append(hist)
        lst.IsA().Destructor(lst)
        return histograms

    @classmethod
    def save(klass, obj, fname="output.root",
             selection="", option="recreate"):
        ofile = ROOT.TFile(fname, option)

        if not selection:
            obj.Write()
            ofile.Close()

        olist = ROOT.TList()
        olist.SetOwner(True)
        cloned = clone(obj, "")
        olist.Add(cloned)
        olist.Write(selection, 1)
        ofile.Close()

    @classmethod
    def read_from_canvas(self, canvas):
        stack = canvas.FindObject("mainpad").FindObject("test")
        return stack.GetHists()

    @classmethod
    def hepdata(klass, record, ofilename, table="Table 1"):
        if os.path.isfile(ofilename):
            return

        link = "https://www.hepdata.net/download/table/{}/{}/1/root"
        try:
            download = link
            url = download.format(record, table.replace(" ", ""))
            response = urllib.request.urlopen(url)

            with open(ofilename, "wb") as f:
                f.write(response.read())
        except urllib.error.HTTPError as e:
            raise IOError("HTTP error {0}\nInvalid record {1}\n{2}"
                          .format(e.code, record, download.format(record)))

        except urllib.error.URLError as e:
            raise IOError("URL error {0}\nInvalid record {1}\n{2}"
                          .format(e.code, record, download.format(record)))


@contextmanager
def tfile(filename, option=""):
    if not os.path.isfile(filename):
        raise IOError("No such file: {0}".format(filename))

    rfile = ROOT.TFile(filename, option)
    yield rfile
    rfile.Close()


def BH(THnT, *args, **kwargs):
    hist = THnT(*args)
    setp(hist, _prop(**kwargs))
    return hist


def setp(dest, source=None, force=False):
    if not source:
        source = _prop()
    _prop.copy(dest, source, force)


def clone(hist, name="_copied", replace=False):
    name = name if replace else hist.GetName() + name
    cloned = hist.Clone(name)
    prop = hist if _prop.has_properties(hist) else _prop()
    setp(cloned, prop)
    return cloned


def copy(hist, name="_copied", replace=False):
    hist = clone(hist, name, replace)
    hist.Reset()
    return hist


def projection(hist, a, b, axis="x"):
    name = "{}_{}_{}".format(hist.GetName(), a, b)

    # NB:  By default ProjectionX takes the last bin as well.
    #      We don"t want to take last bin as it contains the
    #      beginning of the next bin. Therefore use "b - 1" here!
    #

    projection = hist.ProjectionX if axis.lower() == "x" else hist.ProjectionY
    project = hist.ProjectionX if axis.lower() == "x" else hist.ProjectionY
    projection = project(name, a, b - 1)
    setp(projection, hist, force=True)
    return projection


def project_range(hist, xa, xb, axis="x"):
    bin = bincenterf(hist, "x" not in axis)
    return projection(hist, bin(xa), bin(xb), axis)


def same(hist1, hist2):
    if _prop.has_properties(hist1):
        return _prop.same_as(hist2, hist1)

    if _prop.has_properties(hist2):
        return _prop.same_as(hist1, hist2)

    raise AttributeError(
        "Neither of hist1 and hist2 have BROOT properties")


def ratio(a, b, option="B", loggs=None):
    ratio = a.Clone("ratio" + a.GetName())
    _prop.copy_everything(ratio, a)

    # if ratio.GetNbinsX() != b.GetNbinsX():
    # ratio, b = rebin_as(ratio, b)
    if type(b) == ROOT.TF1:
        ratio.Divide(b)
    else:
        ratio.Divide(a, b, 1, 1, option)

    titles = a.GetYaxis().GetTitle().strip(), b.GetYaxis().GetTitle().strip()
    if not any(titles):
        try:
            label = a.label + " / " + b.label
        except AttributeError:
            label = ""
    else:
        label = "{} / {}".format(*titles)
    ratio.GetYaxis().SetTitle(label)
    if not ratio.GetSumw2N():
        ratio.Sumw2()

    return ratio


def set_nevents(hist, nevents, norm=False):
    hist.nevents = nevents
    if norm:
        hist.Scale(1. / nevents)


def rebin_as(hist1, hist2):
    if type(hist2) == ROOT.TF1:
        return hist1, hist2

    if hist1.GetNbinsX() == hist2.GetNbinsY():
        return hist1, hist2

    def nbins(x):
        return x.GetNbinsX()

    a, b = (hist1, hist2) if nbins(
        hist1) > nbins(hist2) else (hist2, hist1)
    rebinned = rebin_proba(a, edges(b))
    return (rebinned, b) if a == hist1 else (b, rebinned)


def rebin_proba(hist, edges, name="_rebinned"):
    edges = array.array("d", edges)
    rebin = hist.Rebin(len(edges) - 1, hist.GetName() + name, edges)

    if not rebin.GetSumw2N():
        rebin.Sumw2()

    for i in range(1, len(edges)):
        delta = edges[i] - edges[i - 1]
        rebin.SetBinContent(i, rebin.GetBinContent(i) / delta)

    if _prop.has_properties(hist):
        setp(rebin, hist, force=True)
    return rebin


def hsum(histograms, label=None):
    if not histograms:
        raise ValueError("You are trying to sum 0 histograms")

    first = histograms[0]
    label = label if label else first.label

    result = copy(first, label)
    setp(result, first)
    result.label = label

    # Finally sum the histograms
    for h in histograms:
        result.Add(h)

    return result


def scalew(hist, factor=None):
    if type(hist) == ROOT.TF1:
        return

    if factor is None:
        factor = min(hist.GetBinWidth(i) for i in hrange(hist))
    hist.Scale(factor, "width")
    return hist


def scalewidth(hist):
    if not hist.GetSumw2N():
        hist.Sumw2()

    for i in hrange(hist):
        width = hist.GetBinWidth(i)
        hist.SetBinContent(i, hist.GetBinContent(i) / width)
    return hist


def scale_clone(hist, scale=1.0):
    scaled = hist.Clone()
    scaled.Scale(scale)
    return scaled


def bincenterf(hist, isxaxis=True):
    axis = hist.GetXaxis() if isxaxis else hist.GetYaxis()
    return lambda x: axis.FindBin(x)


def area_and_error(hist, a, b):
    if a == b:
        return 0, 0
    area, areae = ROOT.Double(), ROOT.Double()
    bin = bincenterf(hist)
    area = hist.IntegralAndError(bin(a), bin(b), areae)
    return area, areae


def init_inputs(func):
    def f(self, hists, *args, **kwargs):
        for h in hists:
            if not h:
                continue
            setp(h)
        return func(self, hists, *args, **kwargs)
    return f


def icolor(i, offset=0):
    return BR_COLORS[(i + offset) % len(BR_COLORS)]


def bins(hist):
    contents = np.array([hist.GetBinContent(i) for i in hrange(hist)])
    errors = np.array([hist.GetBinError(i) for i in hrange(hist)])
    centers = np.array([hist.GetBinCenter(i) for i in hrange(hist)])
    HistMatrix = namedtuple(
        "HistMatrix", ["contents", "errors", "centers"])
    return HistMatrix(contents, errors, centers)


def hist2dict(hist):
    binsdict = bins(hist)._asdict()
    return {k: list(v) for k, v in six.iteritems(binsdict)}


def systematic_deviation(histograms):
    matrix = np.array([bins(h)[0] for h in histograms])

    rms, mean = np.std(matrix, axis=0), np.mean(matrix, axis=0)

    setp(histograms[0])
    syst = copy(histograms[0], "RMS/mean")
    syst.GetYaxis().SetTitle("rms/mean")
    syst.label = "yield extraction"

    for i, r in enumerate(rms / mean):
        syst.SetBinContent(i + 1, r)

    return syst, rms, mean


def hrange(hist, axis="x", start=1, edges=False):
    nbins = hist.GetNbinsX() if "x" in axis.lower() else hist.GetNbinsY()
    # NB: Default value should be 1
    #     one should use 0 if bin edges are needed
    return range(start, nbins + 1 + int(edges))


def pars(tfunc, npars=None):
    if not npars:
        npars = tfunc.GetNpar()

    pp = [tfunc.GetParameter(i) for i in range(npars)]
    ep = [tfunc.GetParError(i) for i in range(npars)]

    FitPars = namedtuple("FitPars", ["pars", "errors"])
    return FitPars(pp, ep)


def empty_bins(hist, tolerance=1e-10):
    return [i for i in hrange(hist)
            if hist.GetBinContent(i) < tolerance]


def diff(hist1, hist2, tol=1e-10):
    bins1, errors1, centers = bins(hist1)
    bins2, errors2, centers = bins(hist2)

    def kernel(x, y):
        return abs(x - y) < tol

    bins_ok = map(kernel, bins1, bins2)
    errors_ok = map(kernel, errors1, errors2)
    return all(bins_ok) and all(errors_ok)


def set_to_zero(hist, rrange):
    a, bb = rrange

    # NB: It should be reversed indicating that we want to
    #     keep have clean interface for spmc: weight, (0, 1) - range
    #

    bins = list(b for b in hrange(hist)
                if not (a < hist.GetBinCenter(b) < bb))
    # NB: Don"t include the last bin,
    #     othervise we will count twice the same point
    #     in sum_trimm method

    # TODO: Check this!?
    for bin in bins:
        hist.SetBinContent(bin, 0)
        hist.SetBinError(bin, 0)


def sum_trimm(hists, ranges):
    clones = list(map(clone, hists))
    for c, r in zip(clones, ranges):
        set_to_zero(c, r)

    return hsum(clones)


def confidence_intervals(hist, func, options="R", histbining=None):
    ci = copy(histbining or hist)
    hist.Fit(func, options + "Q")
    ROOT.TVirtualFitter.GetFitter().GetConfidenceIntervals(ci)
    ci.SetStats(False)
    ci.SetOption("E3")
    ci.SetFillColor(3)
    return ci


def function2histogram(func, hist, scale=1):
    newhist = copy(hist)
    for b in hrange(hist):
        newhist.SetBinContent(b, func.Eval(hist.GetBinCenter(b) * scale))
    return newhist


def chi2(hist1, hist2, rrange=None):
    assert hist1.GetNbinsX() == hist2.GetNbinsX(), \
        "Histograms should have the same binning"
    difference = copy(hist1, "difference")
    difference.Add(hist2, hist1, -1)

    def within_range(x):
        if not rrange:
            return True
        a, b = rrange
        return a < x < b

    chi2 = [
        (b / err) ** 2
        for b, err, center in zip(*bins(difference))
        if within_range(center)
    ]
    chi2 = sum(chi2)
    return chi2


def chi2ndf(hist1, hist2):
    assert hist1.GetNbinsX() > 0, \
        "Histograms should have more than 0 bins"

    return chi2(hist1, hist2) / hist1.GetNbinsX()


# Use multipledispatch
def chi2ndff(func):
    ndf = func.GetNDF()
    if ndf == 0:
        ndf = 1
    return func.GetChisquare() / ndf


def hist_range(hist):
    x = hist.GetXaxis()
    return (
        hist.GetBinCenter(x.GetFirst()),
        hist.GetBinCenter(x.GetLast())
    )


def vec_to_bins(data):
    nbins = len(data)
    step = (max(data) - min(data)) / nbins
    return nbins, min(data) - 0.5 * step, max(data) + 0.5 * step


def average(histograms, label=None):
    summed = hsum(histograms, label)
    summed.Scale(1. / len(histograms))
    summed.GetYaxis().SetTitle(
        "< {} >".format(histograms[0].GetYaxis().GetTitle())
    )
    return summed


def chi2errors(histogram, scale=1):
    functions = histogram.GetListOfFunctions()
    if functions.GetSize() == 0:
        raise ValueError("Histogram should be fitted")

    function = functions.At(0)
    for i in hrange(histogram):
        x = histogram.GetBinCenter(i)
        value = histogram.GetBinContent(i)
        sigma = histogram.GetBinError(i)
        chi2 = ((value - function.Eval(x)) / sigma) ** 2
        histogram.SetBinError(i, chi2 * scale)
    return histogram


def hist2array(hist):
    data = bins(hist)
    return data.contents


def bin_centers(hist):
    centers = copy(hist, "_centers")
    centers.Sumw2()
    for i in hrange(centers):
        centers.SetBinContent(i, centers.GetBinCenter(i))
    return centers


def divide_by_bin_centers(hist):
    centers = bin_centers(hist)
    divided = ratio(hist, centers, option="")
    divided.SetTitle(hist.GetTitle())
    divided.GetXaxis().SetTitle(hist.GetXaxis().GetTitle())
    divided.GetYaxis().SetTitle(hist.GetYaxis().GetTitle())
    return divided


def unity(hist):
    ones = copy(hist)
    for i in hrange(ones):
        ones.SetBinContent(i, 1)
        ones.SetBinError(i, 0)
    return ones


def tf1_sum(func1, func2, name="sum"):
    np1, np2 = func1.GetNpar(), func2.GetNpar()
    start, stop = ROOT.Double(), ROOT.Double()
    func1.GetRange(start, stop)

    def summed(x, par):
        par = array.array("d", par)
        return func1.EvalPar(x, par[:np1]) + func2.EvalPar(x, par[np1:])

    return ROOT.TF1(name, summed, start, stop, np1 + np2)


def edges(x):
    return [x.GetBinLowEdge(i) for i in hrange(x, edges=True)]


def same_binning(hist1, hist2):
    edges1, edges2 = edges(hist1), edges(hist2)
    if len(edges1) != len(edges2):
        return False
    return np.allclose(edges1, edges2)


def unbufer(iterable):
    return [x for x in iterable]


def graph(title, x, y, dx=None, dy=None):
    if dx is None:
        dx = np.zeros_like(x)

    if dy is None:
        dy = np.zeros_like(y)

    graph = ROOT.TGraphErrors(
        len(y),
        array.array('d', x),
        array.array('d', y),
        array.array('d', dx),
        array.array('d', dy),
    )
    graph.SetTitle(title)
    return graph


def graph2hist(graph, hist=None):
    if hist is None:
        centers = unbufer(graph.GetX())
        widths = [(b - a) / 2 for a, b in zip(centers[:-1], centers[1:])]
        widths.append(widths[-1])
        edges = [c - w for c, w in zip(centers, widths)]
        edges.append(edges[-1] + widths[-1])
        hist = ROOT.TH1F("graph", "", len(edges) - 1, array.array('d', edges))

    values = unbufer(graph.GetY())
    for i, v in zip(hrange(hist), values):
        hist.SetBinContent(i, v)
        hist.SetBinError(i, graph.GetErrorY(i - 1))
    return hist


def hist2graph(hist):
    contents, errors, centers = bins(hist)
    hgraph = graph(hist.GetTitle(), x=centers, y=contents, dy=errors)
    hgraph.GetXaxis().SetTitle(hist.GetXaxis().GetTitle())
    hgraph.GetYaxis().SetTitle(hist.GetYaxis().GetTitle())
    hgraph.SetLineColor(hist.GetLineColor())
    hgraph.SetMarkerColor(hist.GetMarkerColor())
    hgraph.SetMarkerStyle(hist.GetMarkerStyle())
    return hgraph


def fit_results(fitf):
    results = {}
    results["#chi^{2}/ndf"] = fitf.GetChisquare() / fitf.GetNDF()
    for i in range(fitf.GetNpar()):
        results[fitf.GetParName(i)] = fitf.GetParameter(i)
        results["#Delta {}".format(fitf.GetParName(i))] = fitf.GetParError(i)
    return results


def print_fit_results(fitf):
    for title, val in fit_results(fitf).items():
        print("{} = {:.3f}".format(title, val))


def shaded_region(title, lower, upper,
                  fill_color=16, fill_style=1001,
                  option="f"):
    x_lower = np.linspace(lower.GetXmin(), lower.GetXmax(), lower.GetNpx())
    y_lower = np.array(list(map(lower.Eval, x_lower)))
    x_upper = np.linspace(upper.GetXmin(), upper.GetXmax(), upper.GetNpx())
    x_upper = x_upper[::-1]
    y_upper = np.array(list(map(upper.Eval, x_upper)))
    x = np.concatenate([x_lower, x_upper])
    y = np.concatenate([y_lower, y_upper])
    graph = ROOT.TGraph(len(x), x, y)
    graph.SetTitle(title)
    graph.SetFillStyle(fill_style)
    graph.SetFillColor(fill_color)
    graph.SetFillColorAlpha(fill_color, 0.36)
    graph.GetDrawOption = lambda: option
    return graph


def shaded_region_hist(title, lower, upper,
                       fill_color=16, fill_style=1001,
                       option="f"):
    y_upper, _, x_upper = bins(upper)
    y_lower, _, x_lower = bins(lower)
    x_upper = x_upper[::-1]
    y_upper = y_upper[::-1]
    x = np.concatenate([x_lower, x_upper])
    y = np.concatenate([y_lower, y_upper])
    graph = ROOT.TGraph(len(x), x, y)
    graph.SetTitle(title)
    graph.SetFillStyle(fill_style)
    graph.SetFillColor(fill_color)
    graph.SetFillColorAlpha(fill_color, 0.36)
    graph.GetDrawOption = lambda: option
    return graph


def auto_color_marker(index=0):
    color = BR_COLORS[index % len(BR_COLORS)]
    marker = 20 + index // len(BR_COLORS)
    return color, marker


def spell(text):
    if text == "#pi^{0}":
        return "pion"
    if text == "#eta":
        return "eta"
    return text


def report(func, particle="", limits=False):
    particle = spell(particle)
    pattern = r"\def \{particle}{func}{par}{err} {{{val:.3g}}}"
    for i in range(func.GetNpar()):
        print(pattern.format(
            particle=particle,
            func=func.GetName(),
            par=func.GetParName(i),
            val=func.GetParameter(i),
            err=""
        ))
        print(pattern.format(
            particle=particle,
            func=func.GetName(),
            par=func.GetParName(i),
            val=func.GetParError(i),
            err="Error"
        ))

    print(r"\def \{particle}{func}Chi {{{val:.3g}}}".format(
        particle=particle,
        func=func.GetName(),
        val=func.GetChisquare() / func.GetNDF()
    ))

    if not limits:
        return

    xmin, xmax = ROOT.Double(0), ROOT.Double(0)
    func.GetRange(xmin, xmax)

    print(r"\def \{particle}{func}MinPt {{{val:.3g}}}".format(
        particle=particle,
        func=func.GetName(),
        val=xmin
    ))

    print(r"\def \{particle}{func}MaxPt {{{val:.3g}}}".format(
        particle=particle,
        func=func.GetName(),
        val=xmax
    ))
