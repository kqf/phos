import ROOT


def wait(name, draw):
    canvas = ROOT.gROOT.FindObject('c1')
    canvas.Update()
    canvas.SaveAs('results/' + name + '.pdf')

    canvas.Connect("Closed()", "TApplication", ROOT.gApplication, "Terminate()")
    if draw: ROOT.gApplication.Run(True)


def draw_and_save(histograms, name = '', draw = True):
    histograms = [h.Clone(h.GetName() + str(id(h))) for h in histograms]
    if name: 
        for h in histograms: h.SetTitle(name.replace('_', ' '))

    histograms[0].Draw()
    for h in histograms: h.Draw('same')
    wait(name + '_' + histograms[0].GetName(), draw)

       
def nicely_draw(hist, option = '', legend = None):
    hist.Draw(option)

    if 'spectrum' in hist.GetName(): 
        ROOT.gPad.SetLogy()
    else:
        ROOT.gPad.SetLogy(0)

    legend = legend if legend else ROOT.TLegend(0.9, 0.4, 1.0, 0.6)
    legend.SetBorderSize(0)
    legend.SetFillStyle(0)
    legend.SetTextSize(0.04)
    legend.AddEntry(hist, hist.label)
    legend.Draw('same')
    wait('xlin_' + hist.GetName(), draw = True)
  