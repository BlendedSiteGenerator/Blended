import os
import shutil

import pkg_resources


def createFolder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)


def getVersion():
    return str(pkg_resources.require("blended")[0].version)


def replaceFolder(folder):
    if os.path.exists(folder):
        shutil.rmtree(folder)
        os.makedirs(folder)
    else:
        os.makedirs(folder)


def returnNone(text):
    if text == "":
        return "NONE"
