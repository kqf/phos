# Order-only prerequisite is marked by "|" character

PERIOD=LHC16g
NAME=$(shell echo $(PERIOD) | tr A-Z a-z)-muon-calo-pass1-2gev-good
DIRECTORY=../$(NAME)

allplots: | $(DIRECTORY)/trending.root $(DIRECTORY)/CaloCellsQA.root
	root -l -b -q  getCellsRunsQAPHOS.C'("$(DIRECTORY)/CaloCellsQA.root")'
	mkdir -p $(NAME)
	mv *.pdf $(NAME)
	mv *.png $(NAME)
	# ls -ltr

$(DIRECTORY)/trending.root: | $(DIRECTORY)/CaloCellsQA.root
	mkdir -p $(NAME)
	mkdir -p fits
	./form-trending-plots.py $(DIRECTORY)
	rm -fr $(NAME)/fits # delete old version
	mv fits $(NAME)/

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
	mv *.pdf $(NAME)/

	montage -tile 4x1 $(NAME)/hPi0Slice*.png  -geometry +0+0 $(NAME)/pi0fits.png
	convert -resize 999x333 $(NAME)/pi0fits.png $(NAME)/pi0fits.png
	montage -tile 4x1 $(NAME)/hMassSM{1..4}.png  -geometry +0+0 $(NAME)/totmass.png
	convert -resize 999x333 $(NAME)/totmass.png $(NAME)/totmass.png
	convert $(NAME)/hNEventsPerRunIndex.png $(NAME)/'ClusterAveragesRuns_NC1_Emin=*_corr4accept.png' $(NAME)/hPi0NumRuns.png $(NAME)/hPi0MassSigmaRuns.png $(NAME)/pi0fits.png $(NAME)/totmass.png -append $(NAME)/$(NAME).png
	# mv *.png pictures

	#rm *.png
