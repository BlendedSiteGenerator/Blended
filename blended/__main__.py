"""This is the Blended Static Website Generator"""
# encoding=utf8
import os
import click
import sys
from sys import platform
import shutil
import pkg_resources
from site_config import check_config, create_config, generate_required_folders

# Very important, get the directory that the user wants to run commands in
cwd = os.getcwd()

try:
    app_version = pkg_resources.require("blended")[0].version
    app_version = app_version[:3]
except:
    app_version = "NOTSET"
    print("WARNING: app_version not set.\n")


@click.group()
def cli():
    """Blended: Static Website Generator"""


@cli.command('init', short_help='Initiate a new website')
def init():
    """Initiates a new website"""

    print("Blended: Static Website Generator -\n")

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

    print("\nThe required files for your website have been generated.")


if __name__ == '__main__':
    cli()
