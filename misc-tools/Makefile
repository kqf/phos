inpconf = config/rules.json

# TODO: add pair operations
# TODO: rewrite for uniformity

.PHONY: clean style test

test:
	$(ROOT_PYTHON) -m unittest discover

style:
	$(ROOT_PYTHON) drawtools/style.py $(inpconf)

clean:
	rm -f *.pdf *.png *.jpg