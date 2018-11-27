DIRECTORY=../results/LHC16/iteration1

images: | $(DIRECTORY)
	python trigger
	mv *.pdf $(DIRECTORY)
	mv *.png $(DIRECTORY)
	mv *.root $(DIRECTORY)

clean:
	rm -rf $(DIRECTORY)

