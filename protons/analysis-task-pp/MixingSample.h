#ifndef MIXINGSAMPLE_H
#define MIXINGSAMPLE_H

// --- Root header files ---

#include <TList.h>
#include <TObject.h>
#include <TObjArray.h>

// --- My Code ---
#include "PhotonSelection.h"

class MixingSample : public TObject
{
public:

	MixingSample(): TObject(), fPool(), fPoolSize(0) {}
	MixingSample(Int_t psize): TObject(), fPool(), fPoolSize(psize) 
	{
		for(Int_t i = 0; i < 10; ++i)
		{
			fPool[i] = new TList(); 
			fPool[i]->SetOwner(kTRUE); 
		}
	}

	virtual ~MixingSample() 
	{
		for(Int_t i = 0; i < 10; ++i)
		{
			if(fPool[i]) delete fPool[i];
		}
	}

	virtual TList * GetPool(EventFlags & e);
	virtual void UpdatePool(const TObjArray & clusters, EventFlags & e); 

protected:
	TList * fPool[10];
	Int_t fPoolSize;

private:
	MixingSample(const MixingSample &); // Not implemented
	MixingSample & operator = (const MixingSample &); // Not implemented

	ClassDef(MixingSample, 1)
};

TList * MixingSample::GetPool(EventFlags & e)
{
	Int_t zbin = Int_t((e.vtxBest[2] + 10.) / 2.); 
	if(zbin < 0) zbin = 0;
	if(zbin > 9) zbin = 9;

	return fPool[zbin];
}   

void MixingSample::UpdatePool(const TObjArray & clusters, EventFlags & e)
{
	TList * pool = GetPool(e);

	if(clusters.GetEntries() > 0)
		pool->AddFirst(clusters.Clone());

	if(pool->GetEntries() > fPoolSize)
	{
		TObject * tmp = pool->Last();
		pool->RemoveLast();
		delete tmp;
	}
}

#endif