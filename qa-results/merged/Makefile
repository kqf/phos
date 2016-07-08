# Order-only prerequisite is marked by "|" character

NAME=lhc16g-muon-calo-pass1-2gev-good
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
	root -l -b -q  getBadMap.C


clean:
	rm *.pdf *.eps *.png

images:
	montage -tile 4x1 hPi0Slice*.png  -geometry +0+0 pi0fits.png
	convert -resize 999x333 pi0fits.png pi0fits.png
	convert 'ClusterAveragesRuns_NC1_Emin=*_corr4accept.png' hPi0NumRuns.png hPi0MassSigmaRuns.png pi0fits.png -append pictures/$(NAME).png
	mv *.png pictures

	#rm *.png
