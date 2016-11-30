LABELS = No_Tender_with_BMap Tender_No_BMap Tender_And_BadMap my_task

images:
	python2 run-pi0-spectrum.py

	for label in $(LABELS); do \
		pdfunite `ls -tr results/ratio*$$label.pdf` results/initial_fit_$$label.pdf; \
		pdfunite `ls -tr results/fit*$$label.pdf` results/signal$$label.pdf; \
		pdfunite `ls -tr results/real*$$label.pdf` results/background_$$label.pdf; \
		rm -f results/real*$$label.pdf results/fit*$$label.pdf results/ratio*$$label.pdf; \
	done
