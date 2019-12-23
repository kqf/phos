from collections import OrderedDict

import spectrum.broot as br


def read_histogram(filename, listname, histname,
                   label='', priority=999, norm=False):
    hist = br.io.read(filename, listname, histname)
    br.set_nevents(hist,
                   Input(filename,
                         listname,
                         histname,
                         label).events(filename, listname),
                   norm)
    hist.priority = priority
    hist.label = label
    return hist


class SingleHistInput(object):

    def __init__(self, histname, listname=None, priority=999, norm=False):
        super(SingleHistInput, self).__init__()
        self.histname = histname
        self.listname = listname
        self.priority = priority
        self.norm = norm

    def transform(self, inputs, loggs=None):
        if type(inputs) == IdentityInput:
            inputs = inputs.single

        hist = br.io.read(
            inputs.filename,
            self.listname or inputs.listname,
            self.histname
        )
        br.set_nevents(hist, inputs.events(
            inputs.filename, inputs.listname), self.norm)
        hist.priority = self.priority
        hist.label = inputs.label
        return hist


class IdentityInput(object):
    def __init__(self, inputs, pt_range, single=None):
        self.inputs = inputs
        self.pt_range = pt_range
        # Input Object for single hist selection
        self.single = single

    def transform(self, data=None, outputs=None):
        return self.inputs


class Input(object):
    def __init__(self, filename, listname,
                 histname='MassPt', pt_range=(0., 20.), label='',
                 mixprefix='Mix', histnames=None,
                 n_events=None, inputs=None,
                 prefix='h'):
        super(Input, self).__init__()
        self.filename = filename
        self.listname = listname
        self.histname = histname
        self.histnames = histnames
        self.mixprefix = '', mixprefix
        self.prefix = prefix
        self._n_events = n_events
        self._events = self.events(filename, listname)
        self.label = label
        self.inputs = inputs
        self.pt_range = pt_range
        if self.inputs:
            return
        self.inputs = ['{}{}{}'.format(self.prefix, p, self.histname)
                       for p in self.mixprefix]

    def events(self, filename, listname):
        try:
            if self._n_events:
                return self._n_events
            return br.io.read(
                filename,
                listname,
                'EventCounter').GetBinContent(2)
        except IOError:
            return -137

    def read(self):
        raw_mix = br.io.read_multiple(
            self.filename,
            self.listname,
            self.inputs
        )

        for h in raw_mix:
            if not h:
                continue
            br.set_nevents(h, self._events)
        return raw_mix

    def read_multiple(self, n_groups=2, single=None):
        data = self.read()
        return [
            IdentityInput(h, self.pt_range, single)
            for h in zip(*(iter(data),) * n_groups)
        ]

    def read_single(self, histname=None):
        histname = histname or self.histname
        hist = br.io.read(self.filename, self.listname, histname)
        return hist

    def transform(self, data=None, outputs=None):
        return self.read()

    @classmethod
    def read_per_module(klass, filename, listname, histname='MassPt',
                        label='', mixprefix='Mix', same_module=False):
        pairs = [(i, j) for i in range(1, 5)
                 for j in range(i, 5) if abs(i - j) < 2]
        if same_module:
            pairs = [pair for pair in pairs if pair[0] == pair[1]]

        names = ['SM{0}SM{1}'.format(*pair) for pair in pairs]

        output = [
            (
                klass(
                    filename,
                    listname,
                    histname + name,
                    label=name,
                    mixprefix=mixprefix
                ),
                name
            ) for name in names]
        return OrderedDict(output)

    def __repr__(self):
        return self.filename


class NoMixingInput(Input):
    def __init__(self, filename, listname, pt_range=(0, 20.),
                 histname='MassPt', *args, **kwargs):
        super(NoMixingInput, self).__init__(filename, listname,
                                            histname, *args, **kwargs)

    def read(self, histo=''):
        histo = histo if histo else self.histname
        raw = br.io.read(self.filename, self.listname, self.prefix + histo)
        br.set_nevents(raw, self._events)
        return raw, None


class ExampleInput(Input):
    def __init__(self, filename, listname='Data',
                 histname='MassPtA10vtx10', mixprefix='Mi'):
        super(ExampleInput, self).__init__(
            filename, listname, histname, mixprefix)

    @staticmethod
    def events(filename, listname):
        return br.io.read(filename, listname, 'hSelEvents').GetBinContent(4)


class TimecutInput(Input):
    def __init__(self, filename, listname, histname, mixprefix='Mix'):
        super(TimecutInput, self).__init__(
            filename, listname, histname, mixprefix)

    @staticmethod
    def events(filename, listname):
        return br.io.read(
            filename,
            'PhysTender',
            'EventCounter'
        ).GetBinContent(2)
