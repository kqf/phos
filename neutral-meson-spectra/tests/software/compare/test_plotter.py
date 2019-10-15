from spectrum.plotter import plot


def test_plotter(data, stop):
    plot(data, "p_{T}", "y", stop=stop)
