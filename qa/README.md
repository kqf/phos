QA scripts
----------

These are all scripts that are needed to extract noisy cells. And inspect ill runs.

# Cell QA analysis

## How to extract noisy channels:
1. Launch `cell-qa-task` from aliphysics with enabled per-run output option (in alien handler).
2. Download and merge/process with tools that are in [scripts directory](cell-qa/scripts)
3. Saved results can be found in [results directory](cell-qa/results)
4. If this is not enough try to use [heatmap method](cell-qa/qa/heatmap) but this one deprecated/redundant. Better to have similar plots in analysis tasks.
Some alternative approaches to timing cut were tested by means of [time-cuts](cell-qa/time-cuts) marcos.

# Trigger QA analysis
## How to run trigger qa:
1. Launch the [tirgger qa task](https://github.com/alisw/AliPhysics/tree/master/PWGGA/PHOSTasks/PHOS_TriggerQA) with enabled per-run output option.
2. Download and merge the histograms with [dedicated macros](trigger-qa/scripts)


