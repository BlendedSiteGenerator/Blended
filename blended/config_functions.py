import json
import os
import sys
from collections import OrderedDict
from shutil import copyfile

from .app_functions import createFolder, getVersion

# Very important, get the directory that the user wants to run commands in
cwd = os.getcwd()


def backupConfig():
    """If the config.json file exists, back it up to config.json.blackup"""
    if checkConfig():
        copyfile(os.path.join(cwd, "config.json"),
                 os.path.join(cwd, "config.json.backup"))


def backupAuthors():
    """If the authors.json file exists, back it up to authors.json.blackup"""
    if checkAuthors():
        copyfile(os.path.join(cwd, "data", "authors.json"),
                 os.path.join(cwd, "data", "authors.json.backup"))


def backupFTP():
    """If the ftp.json file exists, back it up to ftp.json.blackup"""
    if checkFTP():
        copyfile(os.path.join(cwd, "data", "ftp.json"),
                 os.path.join(cwd, "data", "ftp.json.backup"))


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


def checkFTP():
    """Check if the FTP file exists"""
    if os.path.exists(os.path.join(cwd, "data", "ftp.json")):
        return True
    else:
        return False


def createConfig():
    """Create the config file"""
    backupConfig()
    backupAuthors()
    backupFTP()

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
                                            ("description", ""),
                                            ("language", language),
                                            ("theme", ""),
                                            ("build_home", True),
                                            ("build_posts", True),
                                            ("build_pages", True),
                                            ("build_authors", False),
                                            ("build_categories", False),
                                            ("build_tags", False),
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

    ftp = {"server": "serverurl", "username": "yourusername",
           "password": "yourpassword", "port": 21, "upload_path": "public_html/"}

    ftp_file = os.path.join(cwd, "data", "ftp.json")
    with open(ftp_file, 'w') as ftpfile:
        ftpfile.write(json.dumps(ftp, indent=4))


def generateReqFolders():
    """Create the needed folders for a new website"""
    createFolder(os.path.join(cwd, "content"))
    createFolder(os.path.join(cwd, "content", "pages"))
    createFolder(os.path.join(cwd, "content", "posts"))

    createFolder(os.path.join(cwd, "data"))
    createFolder(os.path.join(cwd, "data", "menus"))

    createFolder(os.path.join(cwd, "media"))
    createFolder(os.path.join(cwd, "themes"))
