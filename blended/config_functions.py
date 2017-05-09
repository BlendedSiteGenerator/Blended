import json
import os
import sys
from collections import OrderedDict
from shutil import copyfile

from .app_functions import createFolder, getVersion

# Very important, get the directory that the user wants to run commands in
cwd = os.getcwd()


def backupConfig():
    """If the config.json file exists, it backs it up to config.json.blackup"""
    if checkConfig():
        copyfile(os.path.join(cwd, "config.json"),
                 os.path.join(cwd, "config.json.backup"))

def backupAuthors():
    """If the authors.json file exists, it backs it up to authors.json.blackup"""
    if checkAuthors():
        copyfile(os.path.join(cwd, "data", "authors.json"),
                 os.path.join(cwd, "data", "authors.json.backup"))

def checkConfig():
    """Check if the config file exists"""
    if os.path.exists(os.path.join(cwd, "config.json")):
        return True
    else:
        return False

def checkAuthors():
    """Check if the authors file exists"""
    if os.path.exists(os.path.join(cwd, "data", "authors.json")):
        return True
    else:
        return False

def createConfig():
    backupConfig()
    backupAuthors()

    if sys.version_info < (3, 0):
        title = raw_input("Site Title: ")
        subtitle = raw_input("Site Subtitle: ")
        language = raw_input("Site Language: ")
        authors = raw_input("Author(s): ")
    else:
        title = input("Site Title: ")
        subtitle = input("Site Subtitle: ")
        language = input("Site Language: ")
        authors = input("Author(s): ")

    config_file = os.path.join(cwd, "config.json")
    with open(config_file, 'w') as cfile:
        cfile.write(json.dumps(OrderedDict([("blended_version", str(getVersion())),
                                            ("title", title),
                                            ("subtitle", subtitle),
                                            ("description,", ""),
                                            ("language", language),
                                            ("theme", ""),
                                            ("build_home", True),
                                            ("build_posts", True),
                                            ("build_pages", True),
                                            ("build_authors", False),
                                            ("theme_params", {})]), indent=4))

    authors_list = {}
    for author in authors.split(", "):
        authors_list[author] = {
            "site": "http://test.com",
            "avatar": "userimage.jpg",
            "bio": "All about you goes here.",
            "email": "test@mail.com"
        }

    authors_file = os.path.join(cwd, "data", "authors.json")
    with open(authors_file, 'w') as afile:
        afile.write(json.dumps(authors_list, indent=4))


def generateReqFolders():
    createFolder(os.path.join(cwd, "content"))
    createFolder(os.path.join(cwd, "content", "pages"))
    createFolder(os.path.join(cwd, "content", "posts"))

    createFolder(os.path.join(cwd, "data"))
    createFolder(os.path.join(cwd, "data", "menus"))

    createFolder(os.path.join(cwd, "media"))
    createFolder(os.path.join(cwd, "themes"))
