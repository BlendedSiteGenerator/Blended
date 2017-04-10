"""This holds all of the functions"""
import os
import shutil


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
