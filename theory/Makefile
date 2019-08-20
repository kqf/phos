.PHONY: clean


%.out: %.low.out %.high.out
	cat $^ > $@

result.%.out: param.%.dat
	@# Note that inclnll doesn't accept cli arguments, copy the config
	cp $< param.dat
	docker run --rm -v ${PWD}:/output akqf/incnlo inclnll 

	@# Clean the directory
	rm param.dat
	@mv result.out result.$*.out
	@mv test.out test.$*.out
	@mv error.out error.$*.out

clean:
	rm *.out
