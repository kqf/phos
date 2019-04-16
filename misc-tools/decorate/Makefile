inpconf = config/timing.json

.PHONY: clean style test

test:
	pytest -s

style:
	python drawtools/style.py $(inpconf)

clean:
	rm -f *.pdf *.png *.jpg
