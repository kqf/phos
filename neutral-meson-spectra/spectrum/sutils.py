import os
from collections import Iterable
from contextlib import contextmanager

import ROOT


@contextmanager
def rfile(filename, mode="recreate"):
    fileio = ROOT.TFile(filename, mode)
    yield fileio
    fileio.Close()


def prepare_directory(name):
    path = "/".join(
        name.split("/")[0:-1]  # remove filename
    )

    if not os.path.isdir(path):
        os.makedirs(path, 0755)
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
        canvas.SaveAs(prepare_directory(outdir + name + ".pdf"))
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


def canvas(name="c1", x=1., y=1., scale=6):
    canvas = ROOT.TCanvas(name, "Canvas", int(
        128 * x * scale), int(96 * y * scale))
    ticks(canvas)
    return adjust_canvas(canvas)


# TODO: Change the definition
def gcanvas(x=1., y=1, resize=False, scale=6, name="c1"):
    ccanvas = ROOT.gROOT.FindObject(name)
    if ccanvas:
        if not resize:
            ccanvas.cd()
            return ccanvas

        cx, cy = map(int, [128 * x * scale, 96 * y * scale])
        ccanvas.SetWindowSize(cx, cy)
        ccanvas.SetCanvasSize(cx, cy)
        return adjust_canvas(ccanvas)
    return canvas(name, x, y, scale)


@contextmanager
def tcanvas(name="c1", x=1., y=1., resize=False, scale=6, stop=True):
    canvas = gcanvas(name=name, x=x, y=y, resize=resize, scale=scale)
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
