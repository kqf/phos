import json
import click
import paramiko
from contextlib import contextmanager
from environs import Env
from flatten_dict import flatten

env = Env()
LXPLUS = "lxplus.cern.ch"
LXPLUS_USER = env("LXPLUS_USER")
LXPLUS_HOME = env("LXPLUS_HOME")


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


@click.command()
@click.option('--finput',
              help='Path to the data',
              required=True)
@click.option('--output',
              help='Path to the output files',
              required=True)
def main(finput, output):
    with lxplus_sftp() as sftp:
        filepath = '{}/private/phos/results/{}'.format(LXPLUS_HOME, finput)
        localpath = "{}".format(output)
        sftp.get(filepath, localpath)
