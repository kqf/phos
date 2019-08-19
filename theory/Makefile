.PHONY: clean

result.out: param.dat
	docker run --rm -v ${PWD}:/output akqf/incnlo inclnll

clean:
	rm *.out
