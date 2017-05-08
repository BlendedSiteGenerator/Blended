import os
import sys
import time
import webbrowser

import click

from .app_functions import getVersion
from .build_functions import buildFiles
from .config_functions import createConfig, generateReqFolders
from .content_functions import createPage, createPost
from .ftp_functions import sendFTP
from .theme_functions import downloadTheme, setupTheme

# Very important, get the directory that the user wants to run commands in
cwd = os.getcwd()


@click.group()
@click.version_option(version=getVersion(), message='You are running Blended version %(version)s')
def cli():
    """Blended: Static Website Generator"""


@cli.command('init', short_help="Initate a new website")
def init():
    """Initiates a new website"""

    createConfig()
    generateReqFolders()


@cli.command('download-theme', short_help='Download a theme')
@click.argument('theme')
def download_theme(theme):
    """Download a theme from the Blended themes repository"""

    downloadTheme(theme)


@cli.command('setup-theme', short_help='Setup a theme')
@click.argument('theme')
def setup_theme(theme):
    """Setup a downloaded theme"""

    setupTheme(theme)


@cli.command('view', short_help='View the finished Blended website')
def view():
    """Opens the built index.html file in a web browser"""

    index_path = os.path.realpath(os.path.join(cwd, "build", "index.html"))
    if os.path.exists(index_path):
        webbrowser.open('file://' + index_path)
    else:
        print("The index.html file could not be found in the build folder! Have you deleted it or have you built with buid_homr set to 'false' in config.json?")


@cli.command('ftp', short_help='Upload the build files via ftp')
def send_ftp():
    """Upload the built website to FTP"""

    sendFTP()


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
