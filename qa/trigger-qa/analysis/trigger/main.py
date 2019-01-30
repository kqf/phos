import click
from trend import trend_tru
from channels import channels_tru
from turnoncurves import turn_on_curves


@click.command()
@click.option("--filepath",
              type=click.Path(exists=True),
              help="Where is the dataset",
              required=True)
def main(filepath):
    trend_tru(filepath)
    channels_tru(filepath)
    turn_on_curves(filepath)
