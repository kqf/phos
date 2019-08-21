import re
import click
import six
import pandas as pd
from collections import defaultdict

PATTERNS = {
    "p_T": r"Pt +({float})",
    "#sigma_{total}": r"SIGTOT NLL +({float})",
    "#sigma_{born}": r"where  BORN = +({float})",
    "#sigma_{nlo}": r"HIGH ORDER = +({float})",
    "Kff": r"K factor  fragmentation  NLL/BORN    ({float})"
}
FLOAT = r"[+-]?([0-9]*[.])?[0-9]+"


def parse_incnlo(filename):
    data = defaultdict(list)
    for line in open(filename):
        for title, pattern in six.iteritems(PATTERNS):
            match = re.search(pattern.format(float=FLOAT), line)
            if match:
                data[title].append(float(match.group(1)))
    return data


@click.command()
@click.option("--filename", type=click.Path(exists=True), required=True)
def main(filename):
    data = pd.DataFrame(parse_incnlo(filename))
    print(data)


if __name__ == '__main__':
    main()
