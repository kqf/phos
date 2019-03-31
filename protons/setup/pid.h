#ifndef PID_H
#define PID_H


// Keep this configuration the same for all the analyses
//

AliAnalysisTaskPIDResponse * AddPIDResponse(Bool_t isMC)
{
    AliAnalysisTaskPIDResponse * task = AddTaskPIDResponse(
        isMC,
        kTRUE,
        kTRUE,
        1,          // reco pass
        kFALSE,
        "",
        kTRUE,
        kFALSE,
        1           // reco pass
    );
    return task;
}

#endif
