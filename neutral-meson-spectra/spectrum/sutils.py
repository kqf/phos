import os
import ROOT
from collections import Iterable


def prepare_directory(name):
    path = "/".join(
        name.split('/')[0:-1]  # remove filename
    )

    if not os.path.isdir(path):
        os.makedirs(path, 0755)
    return name


def clean_name(name):
    name = (
        name.strip()
        .replace(' GeV/c', '')
        .replace('p_{T}', 'pT')
        .replace('<', '')
        .replace('>', '')
        .replace('_', '-')
        .replace(',', '-')
        .replace('(', '')
        .replace(')', '')
        .replace('   ', ' ')
        .replace('  ', ' ')
        .replace(' ', '-')
    )
    return name


def wait(name='', draw=True, save=False, suffix=''):
    outdir = 'results/'
    canvas = gcanvas()
    canvas.Update()
    name = clean_name(name)
    if save:
        canvas.SaveAs(prepare_directory(outdir + name + '.pdf'))
        save_canvas(canvas, outdir, name)

    canvas.Connect("Closed()", "TApplication",
                   ROOT.gApplication, "Terminate()")
    if draw:
        ROOT.gApplication.Run(True)


def save_canvas(canvas, outdir, name):
    ofilename = name.split('/')[0]
    hname = name.split('/')[-1]
    path = name.replace(hname, '')
    fname = clean_name(outdir + ofilename.replace("#", "") + ".root")
    path = clean_name(path)
    ofile = ROOT.TFile(fname, "UPDATE")
    ofile.mkdir(path)
    ofile.cd(path)
    canvas.Write(hname)
    ofile.Close()


def canvas(name, x=1., y=1., scale=6):
    canvas = ROOT.TCanvas('c1', 'Canvas', int(
        128 * x * scale), int(96 * y * scale))
    ticks(canvas)
    return adjust_canvas(canvas)


def gcanvas(x=1., y=1, resize=False, scale=6):
    ccanvas = ROOT.gROOT.FindObject('c1')
    if ccanvas:
        if not resize:
            ccanvas.cd()
            return ccanvas

        cx, cy = map(int, [128 * x * scale, 96 * y * scale])
        ccanvas.SetWindowSize(cx, cy)
        ccanvas.SetCanvasSize(cx, cy)
        return adjust_canvas(ccanvas)
    return canvas("c1", x, y, scale)


def fitstat_style():
    ROOT.gStyle.SetStatFontSize(0.1)
    ROOT.gStyle.SetOptStat('')
    ROOT.gStyle.SetStatX(0.35)
    ROOT.gStyle.SetStatW(0.1)
    ROOT.gStyle.SetStatStyle(0)
    ROOT.gStyle.SetStatBorderSize(0)
    ROOT.gStyle.SetOptFit(1)


def adjust_labels(hist1, hist2, scale=1):
    if not hist1 or not hist2:
        return None

    hist1.SetTitleOffset(hist2.GetTitleOffset('X'), 'X')
    hist1.SetTitleOffset(hist2.GetTitleOffset('Y') / scale, 'Y')
    hist1.SetTitleSize(hist2.GetTitleSize('X') * scale, 'X')
    hist1.SetTitleSize(hist2.GetTitleSize('Y') * scale, 'Y')
    hist1.SetLabelSize(hist2.GetLabelSize('X') * scale, 'X')
    hist1.SetLabelSize(hist2.GetLabelSize('Y') * scale, 'Y')
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


class Cc:
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    @staticmethod
    def fail(s):
        return '{0}{1}{2}'.format(Cc.FAIL, s, Cc.ENDC)

    @staticmethod
    def warning(s):
        return '{0}{1}{2}'.format(Cc.warning, s, Cc.ENDC)

    @staticmethod
    def ok(s):
        return '{0}{1}{2}'.format(Cc.OKGREEN, s, Cc.ENDC)
