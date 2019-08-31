.PHONY: tests clean

tests: data.root *.py
	python fit.py

data.root:  *.py
	python generate.py

clean:
	rm *.root
