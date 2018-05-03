#!/usr/bin/python

import sys
import unittest

import ROOT

import spectrum.sutils as st


class TestSpectrumUtils(unittest.TestCase):

    def setUp(self):
        # This is needed to create c1 first from root
        hist = ROOT.TH1F(
            'histWait', 'Test: Drawing with no global canvas', 600, -3, 3)
        hist.Draw()
        self.stop = 'discover' not in sys.argv

    def test_draws_histogram(self):
        hist = ROOT.TH1F(
            'histWait', 'Test: Drawing with no global canvas', 600, -3, 3)
        hist.FillRandom('gaus')
        hist.Draw()
        st.wait(draw=self.stop)

    def test_draws_rescaled(self):
        st.gcanvas(1., resize=True)
        hist = ROOT.TH1F(
            'histNormal', 'Test: Drawing normal scale first', 600, -3, 3)
        hist.FillRandom('gaus')
        hist.Draw()
        st.wait(draw=self.stop)

        st.gcanvas(1. / 2, resize=True)
        hist = ROOT.TH1F(
            'histHalfSize', 'Test: Drawing half-size scale', 600, -3, 3)
        hist.FillRandom('gaus')
        hist.SetLineColor(37)
        hist.Draw()
        st.wait(draw=self.stop)

        st.gcanvas(1., resize=True)
        hist = ROOT.TH1F('histNormalAgain',
                         'Test: Drawing normal scale again', 600, -3, 3)
        hist.FillRandom('gaus')
        hist.SetLineColor(46)
        hist.Draw()
        st.wait(draw=self.stop)

    def test_doesnt_draw_outiside_the_scope(self):
        def drawfunc():
            st.gcanvas(1., resize=True)
            hist = ROOT.TH1F(
                'histInnerScopeFail',
                'Test: you are not supposed to see this histogram',
                600, -3, 3)
            hist.FillRandom('gaus')
            hist.Draw()
        drawfunc()
        t = ROOT.TText(.5, .5, "This pad should be empty")
        t.SetTextAlign(22)
        t.SetTextColor(ROOT.kRed + 2)
        t.SetTextFont(43)
        t.SetTextSize(40)
        t.Draw()
        st.wait(draw=self.stop)

    def test_draws_outside_the_scope(self):
        def drawfunc():
            st.gcanvas(1., resize=True)
            hist = ROOT.TH1F(
                'histInnerScopeOk',
                'Test: Drawing histogram outiside the inner scope',
                600, -3, 3)
            hist.FillRandom('gaus')
            hist.Draw()
            return hist

        hist = drawfunc()
        st.wait(draw=self.stop)
