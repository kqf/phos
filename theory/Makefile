.PHONY: clean


$(directory)incnlo.root: $(directory)result.out incnlo2root.py
	python incnlo2root.py --filename $< --ofilename $@

$(directory)%.out: $(directory)%.low.out $(directory)%.high.out
	cat $^ > $@

$(directory)result.%.out: $(directory)param.%.dat
	@# Note that inclnll doesn't accept cli arguments, copy the config
	cp $< param.dat
	docker run --rm -v ${PWD}:/output akqf/incnlo

	@# Clean the directory
	rm param.dat
	@mv result.out $(directory)result.$*.out
	@mv test.out $(directory)test.$*.out
	@mv error.out $(directory)error.$*.out

clean:
	rm *.out
