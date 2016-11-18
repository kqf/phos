#include "TParticle.h"
#include "TH1F.h"
#include "TString.h"

#include "AliStack.h"
#include "iostream"

using std::cout;
using std::endl;


class ParticleKinematics
{
public:
    enum PdgCode {kPion = 111, kEta = 221, kOmega = 332, kGamma = 22};
    ParticleKinematics(PdgCode specie): fSpecie(specie), fSpectrum(0), fGammas(0)
    {
        TString name = Name(specie);
        fSpectrum = new TH1F(TString("hgen") +  name, name + " ;p_{T} GeV/c; counts", 250, 0., 25.);
        fGammas = new TH1F(TString("hgenGamma") +  name, name + " #gamma-s ;p_{T} GeV/c; counts", 250, 0, 25);
    }

    ParticleKinematics(ParticleKinematics & r):
        fSpecie(r.fSpecie),
        fSpectrum((TH1F *)r.fSpectrum->Clone()),
        fGammas((TH1F *)r.fGammas->Clone())
    {
    }

    ~ParticleKinematics()
    {
        delete fSpectrum;
        delete fGammas;
    }

    void Fill(AliStack * stack, const TParticle * p)
    {
        Int_t code = p->GetPdgCode();
        if (code == fSpecie) fSpectrum->Fill(p->Pt());
        if (code == kGamma && stack->Particle(p->GetFirstMother())->GetPdgCode() == fSpecie)
            fGammas->Fill(p->Pt());
    }

    void Write()
    {
        fSpectrum->Write();
        fGammas->Write();
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
};