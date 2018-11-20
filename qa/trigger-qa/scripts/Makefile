DIRECTORY=../results/LHC16/iteration1

images: | $(DIRECTORY)
	./draw.sh $(DIRECTORY)
	python trend.py
	python channels.py

$(DIRECTORY):
	mkdir -p $(DIRECTORY)
	./download.sh $(DIRECTORY)
	@echo -e "\x07"

clean:
	rm -rf $(DIRECTORY)

