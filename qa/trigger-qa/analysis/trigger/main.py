import click
from trend import trend
from channels import channels


@click.command()
@click.option("--filepath",
              type=click.Path(exists=True),
              help="Where is the dataset",
              required=True)
def main(filepath):
    trend(filepath)
    channels(filepath)
