import os
import shutil

import pkg_resources


def createFolder(folder):
    """Create a folder if it dosen't exist"""
    if not os.path.exists(folder):
        os.makedirs(folder)


def getVersion():
    """Get the current Blended version"""
    return str(pkg_resources.require("blended")[0].version)


def replaceFolder(folder):
    """Remove and regenerate the given folder"""
    if os.path.exists(folder):
        shutil.rmtree(folder)
        os.makedirs(folder)
    else:
        os.makedirs(folder)


def returnNone(text):
    """Return the text 'None' if the input value is empty"""
    if text == "":
        return "NONE"
