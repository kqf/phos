#ifndef MIXINGSAMPLE_H
#define MIXINGSAMPLE_H

// --- Root header files ---

#include <TList.h>
#include <TObject.h>
#include <TObjArray.h>

class MixingSample : public TObject
{
public:

	MixingSample(): TObject(), fPool(0), fPoolSize(0) {}
	MixingSample(Int_t psize): TObject(), fPool(0), fPoolSize(psize) { fPool = new TList(); fPool->SetOwner(kTRUE); }
	virtual ~MixingSample() { if(fPool) delete fPool; }
	virtual TList * GetPool() { return fPool; }     /* zvtx, centrality ?*/
	virtual void UpdatePool(const TObjArray & clusters /* zvtx, centrality ?*/); 

protected:
	TList * fPool;
	Int_t fPoolSize;

private:
	MixingSample(const MixingSample &); // Not implemented
	MixingSample & operator = (const MixingSample &); // Not implemented

	ClassDef(MixingSample, 1)
};

void MixingSample::UpdatePool(const TObjArray & clusters)
{
	if(clusters.GetEntries() > 1)
		fPool->AddFirst(clusters.Clone());

	if(fPool->GetEntries() > fPoolSize)
		fPool->RemoveLast();
}

#endif