pi0:
	$(ROOT_PYTHON) run-pi0-spectrum.py
	@# $(call save_images, my_map default, results/my-bmap-vs-tender.pdf)

eta:
	$(ROOT_PYTHON) run-eta-spectrum.py

imass:
	$(ROOT_PYTHON) -m unittest test.test_invariant_mass


per-module:
	$(ROOT_PYTHON) -m unittest test.test_check_different_modules
	@# $(call save_images, SM1SM1 SM1SM2 SM2SM2 SM2SM3 SM3SM3 SM3SM4 SM4SM4, results/different-modules)

pileup:
	$(ROOT_PYTHON) -m unittest test.test_check_pileup_contribution
	@# $(call save_images, no_timecut 12.5_ns, results/no_timecut)

assymetry:
	$(ROOT_PYTHON) -m unittest test.test_check_assymetry
	@# $(call save_images, no_timecut 12.5_ns, results/no_timecut)

# These are experimental targets. These tests should be used with care.
timecut:
	$(ROOT_PYTHON) -m unittest test.timecut_optimization

check-cut:
	$(ROOT_PYTHON) -m unittest test.timecut_evaluation

selection:
	$(ROOT_PYTHON) -m unittest test.check_physics_selection


define save_images
	for label in $(1); do \
		pdfunite `ls -tr results/ratio*$$label.pdf` results/initial_fit_$$label.pdf; \
		pdfunite `ls -tr results/fit*$$label.pdf` results/signal$$label.pdf; \
		pdfunite `ls -tr results/real*$$label.pdf` results/background_$$label.pdf; \
		pdfunite results/spectrum.pdf results/mass.pdf results/width.pdf results/chi2ndf.pdf $(2).pdf; \
		rm -f results/real*$$label.pdf results/fit*$$label.pdf results/ratio*$$label.pdf; \
	done
endef


