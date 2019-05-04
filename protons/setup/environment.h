#ifndef ENVIRONMENT_H
#define ENVIRONMENT_H

#ifdef __CLING__
R__ADD_INCLUDE_PATH($ALICE_ROOT)
#include <ANALYSIS/macros/AddTaskPIDResponse.C>

R__ADD_INCLUDE_PATH($ALICE_PHYSICS)
#include <OADB/macros/AddTaskPhysicsSelection.C>
#include <PWGGA/PHOSTasks/PHOS_PbPb/AddAODPHOSTender.C>
#include <PWGGA/PHOSTasks/PHOS_EpRatio/AddTaskPHOSEpRatio.C>
#include <PWGGA/PHOSTasks/PHOS_TriggerQA/macros/AddTaskPHOSTriggerQA.C>
#endif


TString message(const char * title, TString period = "")
{
	TString msg;
	if(period.Length() > 0)
	{
	    msg += period + ", ";
	}

    msg += title;
    msg += ", AliPhysics version:";
    msg += gSystem->Getenv("ALIPHYSICS_VERSION");	

    return msg;
}

#endif
