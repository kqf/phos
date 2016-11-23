LABEL1 = BadMap
LABEL2 = Tender

images:
	python2 run-pi0-spectrum.py

	pdfunite `ls -tr results/ratio*$(LABEL1).pdf` results/initial_fit_$(LABEL1).pdf
	pdfunite `ls -tr results/fit*$(LABEL1).pdf` results/signal$(LABEL1).pdf
	pdfunite `ls -tr results/real*$(LABEL1).pdf` results/background_$(LABEL1).pdf
	rm -f results/real*$(LABEL1).pdf results/fit*$(LABEL1).pdf results/ratio*$(LABEL1).pdf

	pdfunite `ls -tr results/ratio*$(LABEL2).pdf` results/initial_fit_$(LABEL2).pdf
	pdfunite `ls -tr results/fit*$(LABEL2).pdf` results/signal$(LABEL2).pdf
	pdfunite `ls -tr results/real*$(LABEL2).pdf` results/background_$(LABEL2).pdf
	rm -f results/real*$(LABEL2).pdf results/fit*$(LABEL2).pdf results/ratio*$(LABEL2).pdf

	ls -ltr results
