import click
from trend import trend, trend_tru
from channels import channels_tru
from turnoncurves import turn_on_curves
from runwise.turnoncurves import turnon_stats


@click.command()
@click.option("--filepath",
              type=click.Path(exists=True),
              help="Where is the dataset",
              required=True)
def main(filepath):
    trend(filepath)
    trend_tru(filepath)
    # channels_tru(filepath)
    # turn_on_curves(filepath)
    turnon_stats(filepath)
