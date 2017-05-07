import os
import sys
import time

import click

from .app_functions import getVersion
from .build_functions import buildFiles
from .config_functions import (backupConfig, checkConfig, createConfig,
                               generateReqFolders)
from .content_functions import createPage, createPost
from .theme_functions import setupTheme

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


@cli.command('setup-theme', short_help='Setup a theme')
@click.argument('theme')
def theme(theme):
    """Setup a downloaded theme"""

    setupTheme(theme)


@cli.command('create', short_help='Create content')
@click.argument('type')
def theme(type):
    """Create content for the website"""

    if type == "post":
        createPost()
    elif type == "page":
        createPage()
    else:
        print("The type you entered was not recognized!")


@cli.command('build', short_help="Build the website")
def build():
    """Builds the website"""

    reload(sys)
    sys.setdefaultencoding('utf8')

    buildFiles()


if __name__ == '__main__':
    cli()
