import spectrum.sutils as su
from spectrum.comparator import Comparator


# NB: This test is needed to check if comparator
#     returns ratio histogram correctly
#     or none object when it's not relevant.

def test_draws_two_histograms(data, stop):
    diff = Comparator(stop=stop)

    data[2].SetTitle('Checking output ratio comparator')
    ratio = diff.compare(data[2], data[1])

    with su.canvas(stop=stop) as canvas:
        canvas.SetLogy(0)
        assert ratio is not None
        ratio.SetTitle("Test Output: This is output ratio plot")
        ratio.Draw()


def test_draws_multiple_histograms(data, stop):
    diff = Comparator(stop=stop)
    data[0].SetTitle('Checking output ratio comparator')
    assert all(diff.compare(arg) for arg in zip(*[data, data]))
