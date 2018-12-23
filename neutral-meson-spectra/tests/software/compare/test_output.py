import spectrum.comparator as cmpr
from spectrum.sutils import wait, gcanvas


# NB: This test is needed to check if comparator
#     returns ratio histogram correctly
#     or none object when it's not relevant.

def test_draws_two_histograms(data, stop):
    diff = cmpr.Comparator(stop=stop)

    data[2].SetTitle('Checking output ratio comparator')
    ratio = diff.compare(data[2], data[1])

    c1 = gcanvas()
    c1.SetLogy(0)
    assert ratio is not None
    ratio.SetTitle("Test Output: This is output ratio plot")
    ratio.Draw()
    wait(stop=stop)


def test_draws_multiple_histograms(data, stop):
    diff = cmpr.Comparator(stop=stop)

    data[0].SetTitle('Checking output ratio comparator')
    assert all(diff.compare(arg) for arg in zip(*[data, data]))
