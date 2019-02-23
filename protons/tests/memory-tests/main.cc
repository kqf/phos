#include <AliAnalysisManager.h>
#include <AliPIDResponseInputHandler.h>
#include <AliMultiInputEventHandler.h>
#include <AliAnalysisTaskPIDResponse.h>
#include <ANALYSIS/macros/AddTaskPIDResponse.C>
// #include <OADB/macros/AddTaskPhysicsSelection.C>
// #include <PWGGA/PHOSTasks/PHOS_PbPb/AddAODPHOSTender.C>
// #include <PWGGA/PHOSTasks/PHOS_EpRatio/AddTaskPHOSEpRatio.C>
// #include <AliPP13TriggerProperties.h>

int main()
{
	for(int i = 0; i < 100; ++i)
		new int();
}
