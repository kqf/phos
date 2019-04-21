.PHONY: all tests

all:
	@which generate > /dev/null || pip install -e .
	generate

tests:
	pytest --cov=phasegen tests/
