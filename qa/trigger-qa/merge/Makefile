year := 2016
period := LHC16g
runlist_file := $(period)_QAresults.list


TRiggerQA.root: $(runlist_file)
	root -b -q ExtractPHOSCellQA.C++'("$<")'

$(runlist_file):
	find /alice/data/$(year)/$(period)/ 000*/pass1/QAresults.root | grep alice | sed "s|/alice|alien:///alice|g" > $@
