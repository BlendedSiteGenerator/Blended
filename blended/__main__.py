"""This is the Blended Static Website Generator"""
# encoding=utf8
import os
import click
import sys
from sys import platform
import shutil
import pkg_resources
from colorama import init as colorama_init
from site_config import check_config, create_config, generate_required_folders
from build_site import build_site
from term_colors import term_colors

colorama_init()

# Very important, get the directory that the user wants to run commands in
cwd = os.getcwd()

try:
    app_version = pkg_resources.require("blended")[0].version
    app_version = app_version[:3]
except:
    app_version = "NOTSET"
    print(term_colors.WARNING + "WARNING: app_version not set.\n" + term_colors.ENDC)


@click.group()
def cli():
    """Blended: Static Website Generator"""


@cli.command('init', short_help='Initiate a new website')
def init():
    """Initiates a new website"""

    print(term_colors.HEADER +
          "Blended: Static Website Generator -\n" + term_colors.ENDC)

    check_config()

    if (sys.version_info > (3, 0)):
        site_title = input("Site Title: ")
        site_tagline = input("Tagline: ")
    else:
        site_title = raw_input("Site Title: ")
        site_tagline = raw_input("Tagline: ")

    # Populate the configuration file
    create_config(app_version=app_version, site_title=site_title,
                  site_tagline=site_tagline)

    generate_required_folders()

    print(term_colors.OKGREEN +
          "\nThe required files for your website have been generated." + term_colors.ENDC)


@cli.command('build', short_help='Build the website files')
def build():
    """Builds the website files"""

    print(term_colors.HEADER +
          "Blended: Static Website Generator -\n" + term_colors.ENDC)

    print(term_colors.OKBLUE + "Building the files!" + term_colors.ENDC)

    build_site()

    print(term_colors.OKGREEN + "The files are built!" + term_colors.ENDC)


if __name__ == '__main__':
    cli()
