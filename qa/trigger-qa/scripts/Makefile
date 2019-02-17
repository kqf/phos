DIRECTORY=../results/LHC16/iteration2

images: | $(DIRECTORY)
	./draw.sh $(DIRECTORY)

$(DIRECTORY):
	mkdir -p $(DIRECTORY)
	./download.sh $(DIRECTORY)
	@echo -e "\x07"

clean:
	rm -rf $(DIRECTORY)
