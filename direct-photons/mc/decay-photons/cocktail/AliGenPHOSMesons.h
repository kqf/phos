#include "AliGenPHOSlib.h"
#include "TF1.h"
#include "TMath.h"

Double_t tsallis(Double_t x, Double_t a, Double_t b, Double_t * p)
{
	return x*p[0]/2./3.1415*(p[2]-1.)*(p[2]-2.)/(p[2]*p[1]*(p[2]*p[1]+b*(p[2]-2.)))*TMath::Power(1.+(TMath::Sqrt(x*x+a*a)-b)/(p[2]*p[1]), -p[2]);
}

class AliGenPHOSMesons: public AliGenPHOSlib
{

public:
	AliGenPHOSMesons() {}
	GenFunc   GetY (Int_t p, const char * ) const {return YPion ;}
	GenFunc   GetV2(Int_t p, const char * ) const {return V2Pion ;}
	GenFuncIp GetIp(Int_t p, const char * ) const 
	{
		switch(p)
		{
			case kPion: return IpPion;
			case kEta: return IpEta;
			case kOmega: return	IpOmega;
			default: return IpPion;
		}
	}

	GenFunc   GetPt(Int_t p, const char * ) const 
	{
		switch(p)
		{
			case kPion: return PtPion;
			case kEta: return PtEta;
			case kOmega: return	PtOmega;
			default: return PtPion;
		}
	}


	static Double_t PtPion(const Double_t * px, const Double_t *)
	{
		Double_t p[] = {2.4, 0.139, 6.88};
		return tsallis(*px, 0.135, 0.135, p);
	}

	static Double_t PtEta(const Double_t * px, const Double_t *)
	{
		Double_t p[] = {0.201, 0.229, 7.};
		return tsallis(*px, 0.547, 0.547, p);
	}

	static Double_t PtOmega(const Double_t * px, const Double_t *)
	{
		Double_t p[] = {1., 0.139, 6.88};
		Double_t x = *px;
		Double_t a = 0.783;
		Double_t b = 0.135;
		return TMath::Sqrt(a*a-b*b+x*x)* tsallis(x, a, b, p);
	}	

	static Int_t    IpPion(TRandom * )   { return 111; }
	static Int_t    IpEta(TRandom * )    { return 221; }
	static Int_t    IpOmega(TRandom * )  { return 223; }

	static Double_t YPion( const Double_t *, const Double_t *) {return 1.;}
	static Double_t V2Pion( const Double_t * /*py*/, const Double_t * /*dummy*/) {return 0.;}

public:
	ClassDef(AliGenPHOSMesons, 1)

} ;
