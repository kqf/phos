DIRECTORY=../results/LHC16/iteration1

images: | $(DIRECTORY)
	python trend.py
	python channels.py

clean:
	rm -rf $(DIRECTORY)

