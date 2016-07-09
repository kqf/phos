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
	montage -tile 4x1 $(NAME)/hPi0Slice*.pdf  -geometry +0+0 $(NAME)/pi0fits.pdf
	convert -resize 999x333 $(NAME)/pi0fits.pdf $(NAME)/pi0fits.pdf
	convert $(NAME)/hNEventsPerRunIndex.pdf $(NAME)/'ClusterAveragesRuns_NC1_Emin=*_corr4accept.pdf' $(NAME)/hPi0NumRuns.pdf $(NAME)/hPi0MassSigmaRuns.pdf $(NAME)/pi0fits.pdf  $(NAME)/$(NAME).pdf
	# mv *.png pictures

	#rm *.png
