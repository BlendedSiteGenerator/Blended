import os
import sys
import time

import click

from .app_functions import getVersion
from .build_functions import buildFiles
from .config_functions import (backupConfig, checkConfig, createConfig,
                               generateReqFolders)

# Very important, get the directory that the user wants to run commands in
cwd = os.getcwd()


@click.group()
@click.version_option(version=getVersion(), message='You are running Blended version %(version)s')
def cli():
    """Blended: Static Website Generator"""


@cli.command('init', short_help="Initate a new website")
def init():
    """Initiates a new website"""

    if checkConfig():
        backupConfig()

    createConfig()
    generateReqFolders()


@cli.command('build', short_help="Build the website")
def build():
    """Builds the website"""

    buildFiles()


if __name__ == '__main__':
    cli()
