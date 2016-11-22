#include "TParticle.h"
#include "TH1F.h"
#include "TH2F.h"
#include "TString.h"

#include "AliStack.h"
#include "iostream"

using std::cout;
using std::endl;


class ParticleKinematics
{
public:
    enum PdgCode {kPion = 111, kEta = 221, kOmega = 332, kGamma = 22, kAny = 1729};
    ParticleKinematics(PdgCode specie): fSpecie(specie), fSpectrum(0), fGammas(0), fhGammaMC(0)
    {
        TString name = Name(specie);
        fSpectrum = new TH1F(TString("hgen") +  name, name + " ;p_{T} GeV/c; counts", 250, 0., 25.);
        fGammas = new TH1F(TString("hgenGamma") +  name, name + " #gamma-s ;p_{T} GeV/c; counts", 250, 0, 25);

        Int_t nPt      = 400;
        Double_t ptMin = 0;
        Double_t ptMax = 40;
        // Todo finish it 
        fhGammaMC = new TH2F(TString("fhGammaMC") + name, Form("MC distribution of #gamma-s from %s;p_{T} GeV/c; #eta", (const char *) name), nPt, ptMin, ptMax, 240, -1.2, 1.2);
    }

    ParticleKinematics(ParticleKinematics & r):
        fSpecie(r.fSpecie),
        fSpectrum((TH1F *)r.fSpectrum->Clone()),
        fGammas((TH1F *)r.fGammas->Clone()),
        fhGammaMC((TH2F *)r.fhGammaMC->Clone())
    {
    }

    ~ParticleKinematics()
    {
        delete fSpectrum;
        delete fGammas;
        delete fhGammaMC;
    }

    void Fill(AliStack * stack, const TParticle * p)
    {
        Int_t code = p->GetPdgCode();
        if (code == fSpecie || fSpecie == kAny) fSpectrum->Fill(p->Pt());
        if (code == kGamma)
        {
            Bool_t condition = stack->Particle(p->GetFirstMother())->GetPdgCode() == fSpecie || fSpecie == kAny;
            if(!condition) 
                return;
            fGammas->Fill(p->Pt());
            fhGammaMC->Fill(p->Pt(), p->Eta());
        }
    }

    void Write()
    {
        fSpectrum->Write();
        fGammas->Write();
        fhGammaMC->Write();
    }

    const char * Name(PdgCode sp) const
    {
        switch (sp)
        {
        case kPion: return "Pi0";
        case kEta: return "Eta";
        case kOmega: return "Omega";
        default: return "";
        }

    }
private:
    PdgCode fSpecie;
    TH1F * fSpectrum;
    TH1F * fGammas;
    TH2F * fhGammaMC;
};