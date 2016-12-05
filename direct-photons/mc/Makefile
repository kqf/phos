ENERGY = 7TeV

fast: double-ratio.py decay-photons/FastGen_pp/generated.root particle-rates.json
	python2 double-ratio.py decay-photons/FastGen_pp/generated.root direct-photons/ $(ENERGY) particle-rates.json

cocktail: double-ratio.py particle-rates.json | decay-photons/cocktail/generated.root
	python2 double-ratio.py decay-photons/cocktail/generated.root direct-photons/ $(ENERGY) particle-rates.json --cocktail

# REMOTE is bash variable that points to my server/lxplus
decay-photons/cocktail/generated.root:
	rsync $(REMOTE)/phos/direct-photons/mc/$@ $@