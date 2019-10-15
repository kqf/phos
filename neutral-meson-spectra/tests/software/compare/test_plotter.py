from spectrum.plotter import plot


def test_plotter(data):
    plot(data, "p_{T}", "y")
