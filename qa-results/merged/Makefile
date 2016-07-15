# Order-only prerequisite is marked by "|" character

PERIOD=LHC16h
NAME=$(shell echo $(PERIOD) | tr A-Z a-z)-muon-calo-pass1-2gev-test
DIRECTORY=../$(NAME)
IM = $(DIRECTORY)/images

allplots: | $(DIRECTORY)/trending.root $(DIRECTORY)/CaloCellsQA.root
	root -l -b -q  getCellsRunsQAPHOS.C'("$(DIRECTORY)/CaloCellsQA.root")'
	mkdir -p $(IM)
	mv *.pdf $(IM)
	mv *.png $(IM)
	# ls -ltr

$(DIRECTORY)/trending.root: | $(DIRECTORY)/CaloCellsQA.root
	mkdir -p $(IM)
	mkdir -p fits
	./form-trending-plots.py $(DIRECTORY)
	rm -fr $(IM)/fits # delete old version
	mv fits $(IM)/

$(DIRECTORY)/CaloCellsQA.root: | $(DIRECTORY)
	# exit
	./merge.py $(DIRECTORY)
	# alienv enter VO_ALICE@AliPhysics::v5-08-08-01-1

pics:
	./draw-pictures.py
	cd pictures;  pdfunite `ls -tr *.pdf` result.pdf

badmap: | $(DIRECTORY)/trending.root $(DIRECTORY)/CaloCellsQA.root
	root -l -b -q  'getBadMap.C("$(PERIOD)")'


clean:
	rm *.pdf *.eps *.png

images:
	make badmap
	mv *.pdf $(IM)/
	montage -tile 4x1 $(IM)/hPi0Slice*.png  -geometry +0+0 $(IM)/pi0fits.png
	convert -resize 999x333 $(IM)/pi0fits.png $(IM)/pi0fits.png
	montage -tile 4x1 $(IM)/hMassSM{1..4}.png  -geometry +0+0 $(IM)/totmass.png
	convert -resize 999x333 $(IM)/totmass.png $(IM)/totmass.png
	convert $(IM)/hNEventsPerRunIndex.png $(IM)/'ClusterAveragesRuns_NC1_Emin=*_corr4accept.png' $(IM)/hPi0NumRuns.png $(IM)/hPi0MassSigmaRuns.png $(IM)/pi0fits.png $(IM)/totmass.png -append $(IM)/$(NAME).png
	# mv *.png pictures

	#rm *.png
