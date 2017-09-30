Datasets, description
---------------------


## How to
In order to check if files available on grid run `check-dataset.sh` macro to verify the dataset.
All missing/corrupted runs will be marked as `[Fail]`. 

Example:
```bash
./check-dataset.sh LHC17f8a.txt

```

## Important:
Always add an extra line at the end of the dataset file.


## Old data ($pp$ 7 TeV)

Data

```
LHC10b.txt
LHC10c.txt
LHC10d.txt
LHC10e.txt
LHC10f.txt
```

Jet-Jet MC
```
LHC15g6b.txt
LHC15g6c.txt
LHC15g6d.txt
LHC15g6e.txt
LHC15g6f.txt
```


## LHC16 data ($pp$ 13 TeV)

### Data
```
LHC16g-muon-calo-pass1.txt
LHC16i-muon-calo-pass1.txt
LHC16l-muon-calo-pass1.txt
LHC16o-muon-calo-pass1.txt
LHC16h-muon-calo-pass1.txt
LHC16j-muon-calo-pass1.txt
LHC16m-muon-calo-pass1.txt
LHC16p-muon-calo-pass1.txt
```

## General-purpose MC ($pp$ 13 TeV)

Pythia

```
LHC16j2a1.txt -> LHC17d20a1.txt
LHC16j2a2.txt -> LHC17d20a2.txt

LHC17d20a1_extra.txt
LHC17d20a2_extra.txt
```

EPOS

```
LHC16j2b1.txt
LHC16j2b2.txt
```

Jet-Jet MC

**NB:**  The production is over, but still the missing runs were not fixed
```
LHC17f8a.txt  (LHC16l)

Missing:
	- 259334 8
	- 259477 8
LHC17f8c.txt  (LHC16g)
	- 254332 8
LHC17f8j.txt  (LHC16h)
LHC17f8d.txt  (LHC16j)
	- 256373 14

LHC17f8f.txt  (LHC16k)
LHC17f8e.txt
	- 262528  (LHC16o)

LHC17f8k.txt  (LHC16p)
LHC17f8g.txt  (LHC16i)
```

The runs that are not anchored to the data taken with phos:
```
LHC17f8b.txt
LHC17f8h.txt
```


## Gamma-Jet MC

Check this dataset, but it shouldn't increase the statistics

```
LHC17i3a1.txt
LHC17i3a2.txt
```



