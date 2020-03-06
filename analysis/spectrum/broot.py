import ROOT
import array
import os
import six
import tqdm
import numpy as np

from collections import namedtuple
from functools import singledispatch
from multimethod import multimethod

from contextlib import contextmanager
from repoze.lru import lru_cache
from six.moves import urllib

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

_PROPERTIES = {
    "label": "",
    "logy": 0,
    "logx": 0,
    "priority": 999,
    "marker": 0
}


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
    if not os.path.isfile(filename) and not option:
        raise IOError("No such file: {0}".format(filename))

    rfile = ROOT.TFile(filename, option)
    yield rfile
    rfile.Close()


def setp(dest, source=_PROPERTIES):
    for key in _PROPERTIES:
        if key in dir(dest):
            continue
        dest.__dict__[key] = source[key]


def clone(hist, name="_copied", replace=False):
    name = name if replace else hist.GetName() + name
    cloned = hist.Clone(name)
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
    return projection


def project_range(hist, xa, xb, axis="x"):
    binc = _bincenterf(hist, "x" not in axis)
    return projection(hist, binc(xa), binc(xb), axis)


@multimethod
def ratio(a, b, option="B", loggs=None):
    ratio = a.Clone("{}_div_{}".format(a.GetName(), b.GetName()))
    ratio.Divide(a, b, 1, 1, option)
    ratio.GetYaxis().SetTitle(
        "{}/{}".format(
            a.GetYaxis().GetTitle().strip(),
            b.GetYaxis().GetTitle().strip()
        )
    )
    if not ratio.GetSumw2N():
        ratio.Sumw2()
    return ratio


@ratio.register(ROOT.TH1, ROOT.TF1)
def _(a, b, option="B", loggs=None):
    ratio = a.Clone("{}_div_{}".format(a.GetName(), b.GetName()))
    ratio.Divide(b)
    if not ratio.GetSumw2N():
        ratio.Sumw2()
    return ratio


def set_nevents(hist, nevents):
    # TODO: Add a separate class for that
    hist.nevents = nevents


def rebin_proba(hist, edges, name="_rebinned"):
    edges = array.array("d", edges)
    rebin = hist.Rebin(len(edges) - 1, hist.GetName() + name, edges)

    if not rebin.GetSumw2N():
        rebin.Sumw2()

    for i in range(1, len(edges)):
        delta = edges[i] - edges[i - 1]
        rebin.SetBinContent(i, rebin.GetBinContent(i) / delta)
    return rebin


def hsum(histograms, label=None):
    if not histograms:
        raise ValueError("You are trying to sum 0 histograms")
    first = histograms[0]
    result = copy(first, first.GetName())
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


def _bincenterf(hist, isxaxis=True):
    axis = hist.GetXaxis() if isxaxis else hist.GetYaxis()
    return lambda x: axis.FindBin(x)


def area_and_error(hist, a, b):
    if a == b:
        return 0, 0
    area, areae = ROOT.Double(), ROOT.Double()
    bin = _bincenterf(hist)
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


@singledispatch
def bins(hist):
    contents = np.array([hist.GetBinContent(i) for i in hrange(hist)])
    errors = np.array([hist.GetBinError(i) for i in hrange(hist)])
    centers = np.array([hist.GetBinCenter(i) for i in hrange(hist)])
    widths = np.array([hist.GetBinWidth(i) for i in hrange(hist)])
    HistMatrix = namedtuple(
        "HistMatrix", ["contents", "errors", "centers", "widths"])
    return HistMatrix(contents, errors, centers, widths)


def hist2dict(hist):
    binsdict = bins(hist)._asdict()
    return {k: list(v) for k, v in six.iteritems(binsdict)}


def systematic_deviation(histograms):
    matrix = np.array([bins(h).contents for h in histograms])

    rms, mean = np.std(matrix, axis=0), np.mean(matrix, axis=0)

    setp(histograms[0])
    syst = copy(histograms[0], "RMS/mean")
    syst.GetYaxis().SetTitle("rms/mean")
    syst.label = "yield extraction"

    for i, r in enumerate(rms / mean):
        syst.SetBinContent(i + 1, r)

    return syst, rms, mean


def maximum_deviation(histograms, central_value=1.):
    matrix = np.array([bins(h).contents for h in histograms])
    normalized = matrix / matrix.mean(axis=0)
    deviations = np.max(np.abs(normalized - 1), axis=0)

    setp(histograms[0])
    syst = copy(histograms[0], "MaxDeviation")
    syst.GetYaxis().SetTitle("Max deviation")

    for i, r in enumerate(deviations):
        syst.SetBinContent(i + 1, r)
    return syst, syst, syst


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
    bins1, errors1, centers, _ = bins(hist1)
    bins2, errors2, centers, _ = bins(hist2)

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
        for b, err, center, _ in zip(*bins(difference))
        if within_range(center)
    ]
    chi2 = sum(chi2)
    return chi2


@multimethod
def chi2ndf(func):
    ndf = func.GetNDF()
    ndf = ndf if ndf > 0 else 1
    return func.GetChisquare() / ndf


@chi2ndf.register(ROOT.TH1F)
def _(hist1, hist2):
    assert hist1.GetNbinsX() > 0, \
        "Histograms should have more than 0 bins"

    return chi2(hist1, hist2) / hist1.GetNbinsX()


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


def edges(x):
    return np.array([x.GetBinLowEdge(i) for i in hrange(x, edges=True)])


def same_binning(hist1, hist2):
    if type(hist1) != type(hist2):
        return False
    edges1, edges2 = edges(hist1), edges(hist2)
    if len(edges1) != len(edges2):
        return False
    return np.allclose(edges1, edges2)


def unbufer(iterable):
    return [x for x in iterable]


@singledispatch
def drawable(graph):
    return graph


@drawable.register(ROOT.TH1)
def _(hist):
    return hist2graph(hist)


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

    hist.GetXaxis().SetTitle(graph.GetXaxis().GetTitle())
    hist.GetYaxis().SetTitle(graph.GetYaxis().GetTitle())
    hist.SetLineColor(graph.GetLineColor())
    hist.SetMarkerColor(graph.GetMarkerColor())
    hist.SetMarkerStyle(graph.GetMarkerStyle())
    return hist


def hist2graph(hist, func=lambda *args: args):
    contents, errors, centers, widths = bins(hist)
    x, y, dx, dy = func(centers, contents, widths, errors)
    hgraph = graph(hist.GetTitle(), x=x, y=y, dx=dx / 2, dy=dy)
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
        results["d{}".format(fitf.GetParName(i))] = fitf.GetParError(i)
    return results


def print_fit_results(fitf):
    for title, val in fit_results(fitf).items():
        print("{} = {:.3f}".format(title, val))


@multimethod
def shaded_region(title, xedges, yedges, fill_color=16, fill_style=1001):
    x = np.concatenate(xedges)
    y = np.concatenate(yedges)
    graph = ROOT.TGraphErrors(len(x), x, y)
    graph.SetTitle(title)
    graph.SetFillStyle(fill_style)
    graph.SetFillColor(fill_color)
    graph.SetFillColorAlpha(fill_color, 0.36)
    # Always plot it with the with the "F" option!
    return graph


@shaded_region.register(str, ROOT.TF1, ROOT.TF1)
def _(title, lower, upper, fill_color=16, fill_style=1001):
    x_lower = np.linspace(lower.GetXmin(), lower.GetXmax(), lower.GetNpx())
    y_lower = np.array(list(map(lower.Eval, x_lower)))
    x_upper = np.linspace(upper.GetXmin(), upper.GetXmax(), upper.GetNpx())
    x_upper = x_upper[::-1]
    y_upper = np.array(list(map(upper.Eval, x_upper)))
    xedges = [x_lower, x_upper]
    yedges = [y_lower, y_upper]
    return shaded_region(title, xedges, yedges, fill_color, fill_style)


@shaded_region.register(str, ROOT.TH1, ROOT.TH1)
def _(title, lower, upper, fill_color=16, fill_style=1001):
    y_upper, _, x_upper, _ = bins(upper)
    y_lower, _, x_lower, _ = bins(lower)
    x_upper = x_upper[::-1]
    y_upper = y_upper[::-1]
    xedges = [x_lower, x_upper]
    yedges = [y_lower, y_upper]
    return shaded_region(title, xedges, yedges, fill_color, fill_style)


def auto_color_marker(index=0, reverse=False, palette=BR_COLORS):
    color = palette[index % len(palette)]
    if reverse:
        color = palette[:3][::-1][index % 3]
    marker = 20 + index // len(palette)
    return color, marker


def spell(text):
    if text == "#pi^{0}":
        return "pion"
    if text == "#eta":
        return "eta"
    return text


def report(func, particle="", limits=False):
    print()
    particle = spell(particle)
    pattern = r"\def \{particle}{func}{par}{err} {{{val:.3f}}}"
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

    print(r"\def \{particle}{func}Chi {{{val:.2f}}}".format(
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


def ratio_uncert(a, b, da, db):
    return (a / b) * ((da / a) ** 2 + (db / b) ** 2) ** 0.5


def module_names(same_module=False):
    pairs = [(i, j) for i in range(1, 5)
             for j in range(i, 5) if abs(i - j) < 2]
    if same_module:
        pairs = [pair for pair in pairs if pair[0] == pair[1]]

    return ['SM{}SM{}'.format(*pair) for pair in pairs]


@contextmanager
def tdirectory(dirname):
    path = ROOT.gDirectory.GetPath()
    ROOT.gDirectory.mkdir(dirname)
    print(path)
    yield ROOT.gDirectory.cd(dirname)
    ROOT.gDirectory.cd(path)


def table2hist(name, title, data, errors, edges, roi=None):
    hist = ROOT.TH1F(name, title, len(edges) - 1, array.array('f', edges))
    for i, (c, error) in enumerate(zip(data, errors)):
        outside_roi = (
            roi is not None and
            roi[0] < hist.GetBinCenter(i + 1) < roi[1]
        )
        if roi is not None:
            if not outside_roi:
                continue
        hist.SetBinContent(i + 1, c)
        hist.SetBinError(i + 1, error)
    return hist


def reset_graph_errors(graph):
    for point in range(graph.GetN()):
        graph.SetPointError(point, 0, graph.GetErrorY(point))
    return graph


class PhysicsHistogram:

    def __init__(self, tot, stat, syst, energy=None):
        self.all = tot, stat, syst
        self.tot = tot
        self.stat = stat
        self.syst = syst
        self.energy = energy
        self._graphs = None

    @property
    def graphs(self):
        if self._graphs:
            return self._graphs
        self._graphs = list(map(hist2graph, self.all))
        # Don't draw "x-errors" for stat. uncertainty
        reset_graph_errors(self.graphs[1])
        return self._graphs

    def Clone(self, title):
        return PhysicsHistogram(
            tot=self.tot.Clone(title),
            stat=self.stat.Clone(title),
            syst=self.syst.Clone(title),
            energy=self.energy,
        )

    def Scale(self, factor):
        for hist in self.all:
            hist.Scale(factor)

    def SetTitle(self, title):
        for hist in self.all:
            hist.SetTitle(title)

    def GetTitle(self):
        return self.tot.GetTitle()

    def GetXaxis(self):
        return self.tot.GetXaxis()

    def GetName(self):
        return self.tot.GetName()

    def GetLineColor(self):
        return self.syst.GetLineColor()

    def Draw(self, option):
        for graph in self.graphs:
            graph.SetFillColorAlpha(0, 0)
        self.graphs[1].Draw("{},pez".format(option))
        self.graphs[2].Draw("{},pe5z".format(option))

    def SetMarkerStyle(self, style):
        for graph in self.graphs:
            graph.SetMarkerStyle(style)

    def SetMarkerSize(self, size):
        for graph in self.graphs:
            graph.SetMarkerSize(size)

    def SetMarkerColor(self, color):
        for graph in self.graphs:
            graph.SetMarkerColor(color)

    def SetLineColor(self, color):
        for graph in self.graphs:
            graph.SetLineColor(color)

    def Fit(self, *args):
        self.tot.Fit(*args)


def from_hepdata(item, cachedir=".hepdata-cachedir"):
    filename = "{}/{}".format(cachedir, item["file"])
    io.hepdata(item["hepdata"], filename, item["table"])
    histnames = ["Graph1D_y1", "Hist1D_y1_e1", "Hist1D_y1_e2"]
    hists = [io.read(filename, item["table"], h) for h in histnames]
    hists[0] = graph2hist(hists[0])

    # The bin contents of Hist1D_y1_e* are the bin errors,
    # which is super strange
    for i, c in enumerate(bins(hists[0]).contents):
        hists[1].SetBinContent(i + 1, c)
        hists[2].SetBinContent(i + 1, c)

    for hist in hists:
        hist.GetXaxis().SetTitle("#it{p}_{T} (GeV/#it{c})")
        hist.SetTitle(item["title"])
        hist.Scale(item["scale"])
        hist.energy = item["energy"]

    measurement = PhysicsHistogram(*hists)
    measurement.energy = item["energy"]
    return measurement


@ratio.register(PhysicsHistogram)
def _(a, b, option="", loggs=None):
    return PhysicsHistogram(
        ratio(a.tot, b, option=option, loggs=loggs),
        ratio(a.stat, b, option=option, loggs=loggs),
        ratio(a.syst, b, option=option, loggs=loggs),
        energy=a.energy,
    )


@ratio.register(PhysicsHistogram, PhysicsHistogram)
def _(a, b, option="", loggs=None):
    return PhysicsHistogram(
        ratio(a.tot, b.tot, option=option, loggs=loggs),
        ratio(a.stat, b.stat, option=option, loggs=loggs),
        ratio(a.syst, b.syst, option=option, loggs=loggs),
    )


@bins.register(PhysicsHistogram)
def _(hist):
    return bins(hist.tot)
