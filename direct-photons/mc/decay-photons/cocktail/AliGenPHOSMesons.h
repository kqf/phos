#include "AliGenPHOSlib.h"
#include "TF1.h"
#include "TMath.h"

class AliGenPHOSMesons: public AliGenPHOSlib
{

public:
	AliGenPHOSMesons() {}
	GenFunc   GetPt(Int_t , const char * ) const {return PtPion ;}
	GenFunc   GetY (Int_t , const char * ) const {return YPion ;}
	GenFunc   GetV2(Int_t , const char * ) const {return V2Pion ;}
	GenFuncIp GetIp(Int_t , const char * ) const {return IpPion ;}

	static Double_t PtPion(const Double_t * px, const Double_t *)
	{
		Double_t p[] = {2.4, 0.139, 6.88};
		Double_t x = *px;
		return x*p[0]/2./3.1415*(p[2]-1.)*(p[2]-2.)/(p[2]*p[1]*(p[2]*p[1]+0.135*(p[2]-2.)))*TMath::Power(1.+(TMath::Sqrt(x*x+0.135*0.135)-0.135)/(p[2]*p[1]), -p[2]);
	}
	static Int_t    IpPion(TRandom * ) { return 111; }
	static Double_t YPion( const Double_t *, const Double_t *) {return 1.;}
	static Double_t V2Pion( const Double_t * /*py*/, const Double_t * /*dummy*/) {return 0.;}

public:
	ClassDef(AliGenPHOSMesons, 1)

} ;
