from output import AnalysisOutput
class TransformerBase(object):

    def __init__(self, plot=False):
        super(TransformerBase, self).__init__()
        self.plot = plot

    def transform(self, inputs, loggs):
    	try:
    		title, stop = loggs
    		loggs = AnalysisOutput(title)
    		plot = True
    	except TypeError:
    		plot = False

        output = self.pipeline.transform(inputs, loggs)

        try:
            if self.plot:
    	        loggs.plot(stop)
        except AttributeError:
            pass

        return output