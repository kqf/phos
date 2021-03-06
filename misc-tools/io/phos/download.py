import os
import json
import click
import paramiko
import tqdm
from contextlib import contextmanager

import six
from environs import Env
from flatten_dict import flatten

env = Env()
LXPLUS = "lxplus.cern.ch"
LXPLUS_USER = env("LXPLUS_USER")
LXPLUS_HOME = env("LXPLUS_HOME")
DATA_PATH = "/phos/analysis"


@contextmanager
def lxplus_sftp():
    host = LXPLUS
    port = 22
    transport = paramiko.Transport((host, port))
    transport.connect(
        username=LXPLUS_USER,
        gss_auth=True,
        gss_kex=True
    )
    sftp = paramiko.SFTPClient.from_transport(transport)
    yield sftp
    sftp.close()
    transport.close()


def extract_targets(finput):
    with open(finput) as f:
        data = json.load(f)
    return [v for k, v in six.iteritems(flatten(data)) if k[-1] == "file"]


def lxplus_path(filename):
    return '{}/private/{}/{}'.format(LXPLUS_HOME, DATA_PATH, filename)


def local_path(ofilename, odirectory):
    filename = '{}/{}'.format(odirectory, ofilename)
    directory = os.path.dirname(filename)
    if not os.path.exists(directory):
        os.makedirs(directory)
    return filename


@click.command()
@click.option('--finput',
              help='Path to the .json with datasets',
              required=True)
@click.option('--output',
              help='Path to the output files',
              required=True)
@click.option('--force',
              help='Force download the file even if the file exists',
              is_flag=True)
def main(finput, output, force):
    targets = extract_targets(finput)
    with lxplus_sftp() as sftp:
        for target in tqdm.tqdm(targets):
            lxplus_target = lxplus_path(target)
            local_target = local_path(target, output)

            if not force and os.path.exists(local_target):
                continue

            try:
                sftp.get(lxplus_target, local_target)
            except FileNotFoundError:
                raise FileNotFoundError(lxplus_target)
