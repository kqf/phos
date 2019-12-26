import spectrum.broot as br

# TODO: Fix this logic, remove Input class


class SingleHistInput(object):

    def __init__(self, histname, listname=None, priority=999, norm=False):
        super(SingleHistInput, self).__init__()
        self.histname = histname
        self.listname = listname
        self.priority = priority
        self.norm = norm

    def transform(self, inputs, loggs=None):
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

        # TODO: Why do we need this?
        for h in raw_mix:
            if not h:
                continue
            br.set_nevents(h, self._events)
        return raw_mix

    def transform(self, data=None, outputs=None):
        return self.read()


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
