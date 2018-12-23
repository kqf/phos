import spectrum.comparator as cmpr


def test_compares_multiple(data, stop):
    diff = cmpr.Comparator(stop=stop)
    data[0].SetTitle('Testing compare set of histograms: explicit')
    diff.compare_set_of_histograms(zip(*[data]))

    data[0].SetTitle('Testing compare set of histograms: "compare"')
    diff = cmpr.Comparator(stop=stop)
    diff.compare(data)


def test_priority(data, stop):
    diff = cmpr.Comparator(stop=stop)

    for h in data:
        h.SetTitle("Checking priority of the histograms")

    data = data[0].Clone()
    data.label = "distorted"

    # Distort the data intentionally
    data.SetBinContent(2, data.GetBinContent(2) * 100)
    data.SetBinContent(55, -1 * data.GetBinContent(55))

    # Without priority
    diff.compare(data[0], data)

    data.priority = 0
    data[0].priority = 999

    # With priority
    diff.compare(data[0], data)


# NB: This is needed to check if behaviour changes
#     after double usage of a comparator. Also this test assures that
#     comparison "A" and "B" and "B" and "A" work as needed.
def test_succesive_comparisons(data, stop):

    diff = cmpr.Comparator(stop=stop)

    data[2].SetTitle("Checking if compare is able to redraw" +
                     "same images properly, Check 1")
    diff.compare(data[2], data[1])

    data[2].SetTitle("Checking if compare is able to redraw" +
                     "same images properly, Check 2")
    diff.compare(data[2], data[1])

    data[1].SetTitle("Checking if compare is able to redraw" +
                     "same images properly: reverse order of histograms")
    diff.compare(data[1], data[2])
