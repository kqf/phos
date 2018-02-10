class MassFitter(object):

    def __init__(self, options, label):
        super(MassFitter, self).__init__()
        self.opt = options

    def transform(self, masses):
        for mass in masses:
            mass.extract_data() 
        return masses
  