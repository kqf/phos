import pytest
import spectrum.comparator as cmpr


def test_different_argument_inputs(data, stop):
    diff = cmpr.Comparator(stop=stop)

    data[0].SetTitle('Compare one single histogram')
    diff.compare(data[0])

    for d in data:
        d.SetTitle('Compare coma separated arguments')
    diff.compare(*data)

    diff = cmpr.Comparator(stop=stop)
    for d in data:
        d.SetTitle('Compare a single list of arguments')
    diff.compare(data)

    diff = cmpr.Comparator(stop=stop)
    diff = cmpr.Comparator(stop=stop)
    for d in data:
        d.SetTitle('Compare two lists of arguments')
    diff.compare(data, data[::-1])

    diff = cmpr.Comparator(stop=stop)
    for d in data:
        d.SetTitle('Compare set of arguments')
    diff.compare(zip(*[data, data]))


def test_handles_wrong_arguments(data, stop):
    diff = cmpr.Comparator(stop=stop)
    for d in data:
        d.SetTitle('Fail')

    with pytest.raises(AssertionError):
        diff.compare(data, [[0]])
