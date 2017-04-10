"""This is the Blended Static Website Generator"""
# encoding=utf8
import os
import click
import sys
from sys import platform
import shutil
import pkg_resources
from config_gen import check_config, create_config

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

    checkConfig()

    if (sys.version_info > (3, 0)):
        site_title = input("Site Title: ")
    else:
        site_title = raw_input("Site Title: ")

    # Populate the configuration file
    createConfig(app_version=app_version, site_title=site_title)

    print("\nThe required files for your website have been generated.")

if __name__ == '__main__':
    cli()
