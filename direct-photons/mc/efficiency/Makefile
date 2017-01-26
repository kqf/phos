SOURCES = AliGenPHOSlib.h AliGenPHOSlibPlus.h Config.C pi0_Param_pp_7TeV.root rec.C sim.C OCDBdrain.tar.gz run.sh run.jdl
REPO=/alice/cern.ch/user/o/okovalen/efficiency


AliESDs.root: $(SOURCES) Kinematics.root
	aliroot -l -b -q rec.C	


Kinematics.root: $(SOURCES)
	aliroot -l -b -q sim.C


.PHONY: clean upload


clean:
	mv pi0_Param_pp_7TeV.root ../
	rm -rf *.ps *.log *.root *.dat *.so *.d
	mv ../pi0_Param_pp_7TeV.root .


upload:
	-alien_mkdir $(REPO)/
	$(foreach file, $(SOURCES), alien_cp -n $(file) alien:$(REPO)/;)
