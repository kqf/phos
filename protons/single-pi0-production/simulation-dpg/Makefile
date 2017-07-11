SEED=1123444

MHOME=/alice/cern.ch/user/o/okovalen
REPO=single-pi0-production
OUTPUT=$(MHOME)/$(REPO)/output/$(SEED)
FILES = dpgsim.sh  generate.jdl tag.C AODtrainsim.C Config.C CreateSnapshot.C QAtrainsim.C rec.C sim.C CheckESD.C ConfigVertexingHF.C DetectorConfig.C ExportGRPinfo.C GeneratorConfig.C OCDBConfig.C ReconstructionConfig.C SimulationConfig.C run-sim.sh

test:
	./single-pion.sh

upload:
	# -alien_rmdir $(MHOME)/$(REPO)
	alien_mkdir -p $(MHOME)/$(REPO)/
	$(foreach file, $(FILES), alien_cp -n $(file) alien:$(MHOME)/$(REPO)/;)

download:
	mkdir -p results 
	for run in $$(alien_ls /$(OUTPUT) | grep .[0-9]*); do alien_cp alien://$(OUTPUT)/$$run/generated.root results/$$run.root; done	
	rm -rf generated.root
	hadd generated.root results/*.root
	rm -rf results
	echo -e "\x07



clean:
	rm -rf tmp_results validation_error.message
	rm -rf *.root *~ *.log *.so *.d *.ps GRP *.dat *.txt *.inp *.xml
	rm -rf 1_1_0_1.stat.aod 1_1_0_1.stat.qa grpdump.sh validation_extrafiles.list
