import ROOT

import os
from collections import Iterable
from contextlib import contextmanager


@contextmanager
def rfile(filename, mode="recreate"):
    fileio = ROOT.TFile(filename, mode)
    yield fileio
    fileio.Close()


def ensure_directory(name):
    directory = os.path.dirname(name)
    if not os.path.exists(directory):
        os.makedirs(directory, 0o755)
    return name


def clean_name(name):
    name = (
        name.strip()
        .replace(" GeV/c", "")
        .replace("p_{T}", "pT")
        .replace("<", "")
        .replace(">", "")
        .replace("_", "-")
        .replace(",", "-")
        .replace("(", "")
        .replace(")", "")
        .replace("   ", " ")
        .replace("  ", " ")
        .replace(" ", "-")
    )
    return name


def show_canvas(canvas, stop=False):
    canvas.Connect("Closed()", "TApplication",
                   ROOT.gApplication, "Terminate()")
    if stop:
        ROOT.gApplication.Run(True)


def wait(stop=False):
    canvas = gcanvas()
    canvas.Update()
    show_canvas(canvas, stop=stop)


def save_canvas(name, pdf=True, root=True):
    outdir = "results/"
    canvas = gcanvas()
    canvas.Update()
    name = clean_name(name)
    if pdf:
        canvas.SaveAs(ensure_directory(outdir + name + ".pdf"))
    if root:
        save_canvas_root(canvas, outdir, name)


def save_canvas_root(canvas, outdir, name):
    ofilename = name.split("/")[0]
    hname = name.split("/")[-1]
    path = name.replace(hname, "")
    fname = clean_name(outdir + ofilename.replace("#", "") + ".root")
    path = clean_name(path)
    ofile = ROOT.TFile(fname, "UPDATE")
    ofile.mkdir(path)
    ofile.cd(path)
    canvas.Write(hname)
    ofile.Close()


def create_canvas(name="c1", size=(128, 96), scale=6):
    canvas = ROOT.TCanvas(name, "canvas",
                          int(size[0] * scale), int(size[1] * scale))
    ticks(canvas)
    return adjust_canvas(canvas)


def gcanvas(name="c1", size=(128, 96), resize=False, scale=6):
    ccanvas = ROOT.gROOT.FindObject(name)
    if ccanvas:
        if not resize:
            ccanvas.cd()
            return ccanvas

        cx, cy = map(int, [size[0] * scale, size[1] * scale])
        ccanvas.SetWindowSize(cx, cy)
        ccanvas.SetCanvasSize(cx, cy)
        return adjust_canvas(ccanvas)
    return create_canvas(name, size, scale)


@contextmanager
def canvas(name="c1", size=(128, 96), resize=False, scale=6, stop=True):
    canvas = gcanvas(name=name, size=size, resize=resize, scale=scale)
    try:
        yield canvas
    finally:
        canvas.Update()
        show_canvas(canvas, stop=stop)


def fitstat_style():
    ROOT.gStyle.SetStatFontSize(0.1)
    ROOT.gStyle.SetOptStat("")
    ROOT.gStyle.SetStatX(0.35)
    ROOT.gStyle.SetStatW(0.1)
    ROOT.gStyle.SetStatStyle(0)
    ROOT.gStyle.SetStatBorderSize(0)
    ROOT.gStyle.SetOptFit(1)


def adjust_labels(hist1, hist2, scale=1):
    if not hist1 or not hist2:
        return None

    hist1.SetTitleOffset(hist2.GetTitleOffset("X"), "X")
    hist1.SetTitleOffset(hist2.GetTitleOffset("Y") / scale, "Y")
    hist1.SetTitleSize(hist2.GetTitleSize("X") * scale, "X")
    hist1.SetTitleSize(hist2.GetTitleSize("Y") * scale, "Y")
    hist1.SetLabelSize(hist2.GetLabelSize("X") * scale, "X")
    hist1.SetLabelSize(hist2.GetLabelSize("Y") * scale, "Y")
    return hist1


def ticks(pad):
    ROOT.gPad.SetGridx()
    ROOT.gPad.SetGridy()
    ROOT.gPad.SetTickx()
    ROOT.gPad.SetTicky()
    pad.SetTickx()
    pad.SetTicky()
    pad.SetGridx()
    pad.SetGridy()
    return pad


def adjust_canvas(canvas):
    height = canvas.GetWindowHeight()
    canvas.SetBottomMargin(0.02 * height)
    canvas.SetTopMargin(0.02 * height)

    width = canvas.GetWindowWidth()
    canvas.SetRightMargin(0.01 * width)
    canvas.SetLeftMargin(0.01 * width)
    return canvas


def equals(a, b, tol=1e-7):
    if isinstance(a, Iterable):
        return all(map(lambda x, y: equals(x, y, tol), zip(a, b)))
    return abs(a - b) < tol


def in_range(x, somerange):
    a, b = somerange
    return a < x < b


def write(tobject, filename, option="recreate"):
    ofile = ROOT.TFile(filename, option)
    tobject.Write()
    ofile.Close()


def spell(text):
    if text == "#pi^{0}":
        return "pion"
    if text == "#eta":
        return "eta"
