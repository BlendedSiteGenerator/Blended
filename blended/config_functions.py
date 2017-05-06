import os
import sys
from shutil import copyfile

from .app_functions import createFolder, getVersion

# Very important, get the directory that the user wants to run commands in
cwd = os.getcwd()


def backupConfig():
    """If the config.json file exists, it backs it up to config.json.blackup"""
    if checkConfig():
        copyfile(os.path.join(cwd, "config.json"),
                 os.path.join(cwd, "config.json.backup"))


def checkConfig():
    """Check if the config file exists"""
    if os.path.exists(os.path.join(cwd, "config.json")):
        return True
    else:
        return False


def createConfig():
    if sys.version_info < (3, 0):
        title = raw_input("Site Title: ")
        subtitle = raw_input("Site Subtitle: ")
        language = raw_input("Site Language: ")
    else:
        title = input("Site Title: ")
        subtitle = input("Site Subtitle: ")
        language = input("Site Language: ")

    config_file = os.path.join(cwd, "config.json")

    with open(config_file, 'w') as cfile:
        cfile.write("{")
        cfile.write("\n")
        cfile.write("\"blended_version\": \"" + getVersion() + "\",")
        cfile.write("\n")
        cfile.write("\"title\": \"" + title + "\",")
        cfile.write("\n")
        cfile.write("\"subtitle\": \"" + subtitle + "\",")
        cfile.write("\n")
        cfile.write("\"language\": \"" + language + "\",")
        cfile.write("\n")
        cfile.write("\"theme\": \"\",")
        cfile.write("\n")
        cfile.write("\"build_home\": true,")
        cfile.write("\n")
        cfile.write("\"build_posts\": true,")
        cfile.write("\n")
        cfile.write("\"build_pages\": true,")
        cfile.write("\n")
        cfile.write("\"build_authors\": false,")
        cfile.write("\n")
        cfile.write("\"theme_params\": {},")
        cfile.write("\n")
        cfile.write("}")


def generateReqFolders():
    createFolder(os.path.join(cwd, "content"))
    createFolder(os.path.join(cwd, "content", "pages"))
    createFolder(os.path.join(cwd, "content", "posts"))

    createFolder(os.path.join(cwd, "data"))
    createFolder(os.path.join(cwd, "data", "menus"))

    createFolder(os.path.join(cwd, "media"))
    createFolder(os.path.join(cwd, "themes"))
