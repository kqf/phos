# To avoid problems with gas composition value from OCDB use older version 
# of aliroot 
# alienv enter VO_ALICE@AliPhysics::vAN-20160705-1

SOURCES = sim.C rec.C

AliESDs.root: $(SOURCES) Kinematics.root
	aliroot -l -b -q rec.C	

Kinematics.root: $(SOURCES)
	aliroot -l -b -q sim.C

