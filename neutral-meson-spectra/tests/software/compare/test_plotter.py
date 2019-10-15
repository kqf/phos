from spectrum.plotter import plot


def test_plotter(data, stop):
    plot(data, "p_{T}", "y", logy=True, logx=True, stop=stop)
