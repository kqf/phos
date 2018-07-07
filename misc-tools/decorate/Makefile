inpconf = config/timing.json

.PHONY: clean style test

test:
	$(ROOT_PYTHON) -m unittest discover

style:
	$(ROOT_PYTHON) drawtools/style.py $(inpconf)

clean:
	rm -f *.pdf *.png *.jpg