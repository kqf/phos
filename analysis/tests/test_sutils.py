import pytest
import ROOT

import spectrum.sutils as su


@pytest.fixture
def background():
    # NB: this is needed to create c1 first from root
    hist = ROOT.TH1F('histW', 'Test: No global canvas', 600, -3, 3)
    hist.Draw()


def test_draws_histogram(stop, background):
    with su.canvas(stop=stop):
        hist = ROOT.TH1F(
            'histW', 'Test: Drawing with no global canvas', 600, -3, 3)
        hist.FillRandom('gaus')
        hist.Draw()


def test_draws_rescaled(stop, background):
    with su.canvas(size=(128., 128), resize=True, stop=stop):
        hist = ROOT.TH1F(
            'histNormal', 'Test: Drawing normal scale first', 600, -3, 3)
        hist.FillRandom('gaus')
        hist.Draw()

    with su.canvas(size=(128. / 2, 128), resize=True, stop=stop):
        hist = ROOT.TH1F(
            'histHalfSize', 'Test: Drawing half-size scale', 600, -3, 3)
        hist.FillRandom('gaus')
        hist.SetLineColor(37)
        hist.Draw()

    with su.canvas(size=(128., 128), resize=True, stop=stop):
        hist = ROOT.TH1F('histNormalAgain',
                         'Test: Drawing normal scale again', 600, -3, 3)
        hist.FillRandom('gaus')
        hist.SetLineColor(46)
        hist.Draw()


def test_doesnt_draw_outiside_the_scope(stop, background):
    def drawfunc():
        with su.canvas(stop=stop):
            hist = ROOT.TH1F(
                'histInnerScopeFail',
                'Test: you are not supposed to see this histogram',
                600, -3, 3)
            hist.FillRandom('gaus')
            hist.Draw()
    drawfunc()
    with su.canvas(stop=stop):
        t = ROOT.TText(.5, .5, "This pad should be empty")
        t.SetTextAlign(22)
        t.SetTextColor(ROOT.kRed + 2)
        t.SetTextFont(43)
        t.SetTextSize(40)
        t.Draw()


def test_draws_outside_the_scope(stop, background):
    def drawfunc():
        with su.canvas(stop=stop):
            hist = ROOT.TH1F(
                'histInnerScopeOk',
                'Test: Drawing histogram outiside the inner scope',
                600, -3, 3)
            hist.FillRandom('gaus')
        return hist
    hist = drawfunc()  # noqa root needs this object
