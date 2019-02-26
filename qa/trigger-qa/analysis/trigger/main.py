from __future__ import print_function

import os
import click
from trigger.trend import trend, trend_tru
from trigger.channels import channels_tru_period
from trigger.channels import channels_tru_total
# from turnoncurves import turn_on_curves
from trigger.turnoncurves import turnon_stats


@click.command()
@click.option("--filepath",
              type=click.Path(exists=True),
              help="Where is the dataset",
              required=True)
def main(filepath):
    trend(filepath)
    trend_tru(filepath)
    channels_tru_period(filepath)
    turnon_stats(filepath)


@click.command()
@click.option("--filepath",
              type=click.Path(exists=True),
              help="Where is the dataset",
              required=True)
def channels(filepath):
    files = [fname for fname in os.listdir(filepath)
             if fname.endswith(".root")]
    paths = [os.path.join(filepath, f) for f in files]
    channels_tru_total(paths)
