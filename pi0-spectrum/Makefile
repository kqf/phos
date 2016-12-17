LABELS = Tender_No_BMap my_task_and_tender my_task_no_tender my_task_only_tender
RESULT = results/1-MyTaskVsTender

images:
	$(ROOT_PYTHON) run-pi0-spectrum.py
	$(call save_images, $(LABELS), $(RESULT))

per-module:
	$(ROOT_PYTHON) -m unittest test.check_different_modules
	$(call save_images, SM1SM1 SM1SM2 SM2SM2 SM2SM3 SM3SM3 SM3SM4 SM4SM4, results/different-modules)

pileup:
	$(ROOT_PYTHON) -m unittest test.check_pileup_contribution
	$(call save_images, no_timecut 23ns, results/timecut)

timecut:
	$(ROOT_PYTHON) -m unittest test.timecut_optimization

define save_images
	for label in $(1); do \
		pdfunite `ls -tr results/ratio*$$label.pdf` results/initial_fit_$$label.pdf; \
		pdfunite `ls -tr results/fit*$$label.pdf` results/signal$$label.pdf; \
		pdfunite `ls -tr results/real*$$label.pdf` results/background_$$label.pdf; \
		pdfunite results/spectrum.pdf results/mass.pdf results/width.pdf results/chi2ndf.pdf $(2).pdf; \
		rm -f results/real*$$label.pdf results/fit*$$label.pdf results/ratio*$$label.pdf; \
	done
endef


