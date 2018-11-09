import json
import hashlib
from spectrum.input import Input, NoMixingInput


class DataVault(object):
    def __init__(self, ledger='ledger.json'):
        super(DataVault, self).__init__()
        with open('config/vault/' + ledger) as f:
            self._ledger = json.load(f)

    @classmethod
    def _validate_dataset(klass, filename, hsum_nominal):
        hashsum = hashlib.sha256()
        with open(filename) as f:
            data = f.read()
        hashsum.update(data)
        hsum_real = hashsum.hexdigest()

        msg = "File {0} doesn't match the desired hash {1} but got {2}".format(
            filename,
            hsum_nominal,
            hsum_real
        )

        if hsum_real != hsum_nominal:
            raise IOError(msg)

    def dataset(self, production, version="latest"):
        return self._ledger[production][version]

    def file(self, production, version="latest"):
        data = self.dataset(production, version)
        filename = data["file"]
        self._validate_dataset(filename, data["hsum"])
        return filename

    def input(self, production, version="latest",
              listname=None, pt_range=None, use_mixing=True,
              *args, **kwargs):

        filename = self.file(production, version)
        if not listname:
            listname = self.dataset(production, version)['default_selection']

        if not pt_range:
            pt_range = self.dataset(production, version)['pt_range']

        transformer = Input if use_mixing else NoMixingInput
        return transformer(filename, str(listname), pt_range=pt_range,
                           *args, **kwargs)

    def modules_input(self, production, version="latest", listname="Phys",
                      same_module=True, *args, **kwargs):
        inputs = Input.read_per_module(
            self.file(production, version),
            listname,
            same_module=same_module
        )
        return inputs

    def validate_all_datasets(self):
        not_valid = []
        for productionion in self._ledger:
            for version in self._ledger[productionion]:
                dataset = self._ledger[productionion][version]
                try:
                    self._validate_dataset(dataset['file'], dataset['hsum'])
                except IOError as e:
                    not_valid.append(
                        (productionion, version, str(e).split()[-1])
                    )
        return not_valid
