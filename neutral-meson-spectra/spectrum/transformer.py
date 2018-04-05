from output import AnalysisOutput
class TransformerBase(object):

    def transform(self, inputs, loggs):
    	try:
    		title, stop = loggs
    		loggs = AnalysisOutput(title)
    		plot = True
    	except TypeError:
    		plot = False

        output = self.pipeline.transform(inputs, loggs)

        if plot:
	        loggs.plot(stop)

        return output