import spectrum.comparator as cmpr


def test_compares_ratios(data, stop):
    """
        This one is needed to compare "double ratio" plots.
    """
    data[0].SetTitle('Test compare: ratios with common baselines')
    diff = cmpr.Comparator(stop=stop)
    diff.compare_ratios(data, data[2])


def test_compares_multiple_ratios(data, stop):
    """
        This one is needed to compare "double ratio"
        plots with different baselines.
        The result of this test should give three constant( = 1) graphs.
    """

    data[0].SetTitle('Test compare: ratios with different baselines')
    diff = cmpr.Comparator(stop=stop)
    diff.compare_multiple_ratios(data, data)
