import spectrum.vis as vi


def test_vis_hub(data, stop):
    vishub = vi.VisHub((1, 1), (), (), stop, '', None)
    data[0].SetTitle('Test ViHub: Testing MultipleVisualizer')
    vishub.compare_visually(data)

    data[0].SetTitle('Test VisHub: MultipleVisualizer')
    vishub.compare_visually(data[0:2])

    data[0].SetTitle('Test VisHub: Single Visualizer')
    vishub.compare_visually([data[0]])


def test_draws_multiple_plots(data, stop):
    vis = vi.VisHub((1, 1), (), (), stop, '', None)

    data[0].SetTitle('Test VisMultiple: Testing MultipleVisualizer')
    vis.compare_visually(data)

    data[0].SetTitle('Test VisMultiple: MultipleVisualizer')
    vis.compare_visually(data[0:2])

    data[0].SetTitle('Test VisMultiple: Test Single')
    vis.compare_visually([data[0]])


def test_handles_double_plots(data, stop):
    vis = vi.VisHub((1, 1), (), (), stop, '', None)
    data[0].SetTitle('Test DoubleVis: Visualize two plots')
    vis.compare_visually(data[0:2])
