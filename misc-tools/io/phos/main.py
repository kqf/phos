import click
from phos.unlist import unlist
from phos.remove2dir import remove2dir


@click.command()
@click.option('--filename',
              type=click.Path(exists=True),
              help='Path to the .root file',
              required=True)
@click.option('--path',
              help='Histogram, example: "Phys/MassPt"',
              required=True)
def munlist(filename, path):
    """
    Flatten the root file with lists, save everything under the root folder
    Usage
    unlist .--filename /path/to/file --path="Phys/MassPt"
    """  # noqa
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
    """
    Flatten the root file with lists, save everything under the root folder
    Usage
    remove2dir --file ./path/to/file --path="PHOSEpRatio/PHOSEpRatioCoutput1"
    """
    remove2dir(filename, path)
