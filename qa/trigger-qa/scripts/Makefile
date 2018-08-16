DIRECTORY=../results/LHC17/
ITERATION="default"


images: | $(DIRECTORY)
	./draw.sh $(DIRECTORY) $(ITERATION)

$(DIRECTORY):
	mkdir -p $(DIRECTORY)
	./download.sh $(DIRECTORY) $(ITERATION)
	@echo -e "\x07"

clean:
	rm -rf $(DIRECTORY)

