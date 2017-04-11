"""This holds all of the functions"""
import os
import sys
import shutil
import ntpath
from term_colors import term_colors


def create_folder(path):
    """Creates the specified folder if it dosen't already exist"""
    if not os.path.exists(path):
        os.makedirs(path)


def replace_folder(path):
    """If the specified folder exists, it is deleted and recreated"""
    if os.path.exists(path):
        shutil.rmtree(path)
        os.makedirs(path)
    else:
        os.makedirs(path)


def force_exist(files, type):
    for wfile in files:
        if not os.path.exists(wfile):
            sys.exit(term_colors.FAIL +
                     "ERROR: You must have a " + ntpath.basename(wfile) + " " + type + "!" + term_colors.ENDC)
