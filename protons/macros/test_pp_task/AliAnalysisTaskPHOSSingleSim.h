#ifndef AliAnalysisTaskPHOSSingleSim_cxx
#define AliAnalysisTaskPHOSSingleSim_cxx

// Author: Daiki Sekihata (Hiroshima University)

class TList;
class AliVEvent;
class AliESDEvent;
class AliAODEvent;
class AliPHOSGeometry;
class TClonesArray;
class AliStack;

#include "AliAnalysisTaskSE.h"

class AliAnalysisTaskPHOSSingleSim : public AliAnalysisTaskSE {
  public:

    AliAnalysisTaskPHOSSingleSim(const char *name = "SingleSim");
    virtual ~AliAnalysisTaskPHOSSingleSim(); 

  protected:
    virtual void UserCreateOutputObjects();
    virtual void UserExec(Option_t *option);
    virtual void Terminate(Option_t *option);
    virtual void ProcessMC();
    void CellQA();
    void ClusterQA();
    void FillPhoton();
    void FillMgg();
    void FillMixMgg();

    void SetMCWeight();//set weight related to M.C. (pT slope of mother pi0/eta/K0S/gamma)
    Int_t FindPrimaryMotherESD(Int_t label);
    Double_t R(AliAODMCParticle *p);//in cylindrical system
    Double_t Rho(AliAODMCParticle *p);//in sperical system


    void FillHistogramTH1(TList *list, const Char_t *name, Double_t x, Double_t w=1., Option_t *opt = "") const ;
    void FillHistogramTH2(TList *list, const Char_t *name, Double_t x, Double_t y, Double_t w=1., Option_t *opt = "") const ;
    void FillHistogramTH3(TList *list, const Char_t *name, Double_t x, Double_t y, Double_t z, Double_t w=1., Option_t *opt = "") const ;
    void FillProfile(TList *list, const Char_t *name, Double_t x, Double_t y) const ;
    void FillSparse(TList *list, const Char_t *name, Double_t *x, Double_t w=1.) const;

    AliStack *GetMCInfoESD();
    TClonesArray *GetMCInfoAOD();


  protected:
    THashList *fOutputContainer;
    AliVEvent *fEvent;
    AliESDEvent *fESDEvent;
    AliAODEvent *fAODEvent;
    AliStack *fMCArrayESD;     //MC particles array in ESD
    TClonesArray *fMCArrayAOD; //MC particles array in AOD
    Int_t fRunNumber;
    AliPHOSGeometry *fPHOSGeo;
    TList *fPHOSEvents[10];
    TClonesArray *fPHOSClusterArray;
    Double_t fVertex[3];
    Int_t fZvtx;

  private:
    AliAnalysisTaskPHOSSingleSim(const AliAnalysisTaskPHOSSingleSim&);
    AliAnalysisTaskPHOSSingleSim& operator=(const AliAnalysisTaskPHOSSingleSim&);

    ClassDef(AliAnalysisTaskPHOSSingleSim, 1);
};

#endif
