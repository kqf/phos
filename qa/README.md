QA scripts
----------

These are all scripts that are needed to extract noisy cells. And inspect ill runs.


## How to extract noisy channels:
1. Launch `qa-task`  with enabled per-run output option (in alien handler).
2. Download and merge/process with tools that are in [scripts directory](/scripts)
3. Saved results can be found in [results directory](/results)
4. If this is not enough try to use [heatmap method](/qa/heatmap) but this one deprecated/redundant. Better to have similar plots in analysis tasks.


## How to run trigger qa:

1. Launch [trigger QA task](/qa-trigger) with enabled per-run output option (in alien handler).
2. Process histograms using [dedicated macros](scripts-trigger)


Some alternative approaches to timing cut were tested by means of [time-cuts](/time-cuts) marcos.