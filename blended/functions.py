import os
import shutil
import urllib
import zipfile


def create_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)


def replace_folder(path):
    if os.path.exists(path):
        shutil.rmtree(path)
        os.makedirs(path)
    else:
        os.makedirs(path)


def get_html_filename(filename):
    if ".html" in filename:
        newFilename = filename
    elif ".md" in filename:
        newFilename = filename.replace(".md", ".html")
    elif ".tile" in filename:
        newFilename = filename.replace(".tile", ".html")
    elif ".jade" in filename:
        newFilename = filename.replace(".jade", ".html")
    elif ".txt" in filename:
        newFilename = filename.replace(".txt", ".html")
    elif ".rst" in filename:
        newFilename = filename.replace(".rst", ".html")
    elif ".docx" in filename:
        newFilename = filename.replace(".docx", ".html")
    else:
        print(filename + " is not a valid file type!")

    return newFilename


def get_html_clear_filename(filename):
    newFilename = filename.replace(".html", "")
    newFilename = newFilename.replace(".md", "")
    newFilename = newFilename.replace(".txt", "")
    newFilename = newFilename.replace(".tile", "")
    newFilename = newFilename.replace(".jade", "")
    newFilename = newFilename.replace(".rst", "")
    newFilename = newFilename.replace(".docx", "")
    newFilename = newFilename.replace("index", "home")
    newFilename = newFilename.replace("-", " ")
    newFilename = newFilename.replace("_", " ")
    newFilename = newFilename.title()

    return newFilename


def getunzipped(theurl, thedir):
    name = os.path.join(thedir, 'temp.zip')
    try:
        name, hdrs = urllib.urlretrieve(theurl, name)
    except IOError, e:
        print "Can't retrieve %r to %r: %s" % (theurl, thedir, e)
        return
    try:
        z = zipfile.ZipFile(name)
    except zipfile.error, e:
        print "Bad zipfile (from %r): %s" % (theurl, e)
        return
    for n in z.namelist():
        dest = os.path.join(thedir, n)
        destdir = os.path.dirname(dest)
        if not os.path.isdir(destdir):
            os.makedirs(destdir)
        data = z.read(n)
        f = open(dest, 'w')
        f.write(data)
        f.close()
    z.close()
    os.unlink(name)
