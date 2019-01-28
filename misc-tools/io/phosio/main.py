import click
from phosio.unlist import unlist
from phosio.remove2dir import remove2dir


@click.command()
@click.option('--filename',
              type=click.Path(exists=True),
              help='Path to the .root file',
              required=True)
@click.option('--path',
              help='Histogram, example: "Phys/MassPt"',
              required=True)
def munlist(filename, path):
    unlist(filename, *path.split("/"))


@click.command()
@click.option('--filename',
              type=click.Path(exists=True),
              help='Path to the .root file',
              required=True)
@click.option('--path',
              help='Histogram, example: "PHOSEpRatio/PHOSEpRatioCoutput1"',
              required=True)
def mremove2dir(filename, path):
    remove2dir(filename, path)
