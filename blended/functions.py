import os
import shutil

def create_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)

def replace_folder(path):
    if os.path.exists(path):
        shutil.rmtree(path)
        os.makedirs(path)
    else:
        os.makedirs(path)
