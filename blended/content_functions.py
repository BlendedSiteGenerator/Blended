import itertools
import os
import sys

from .app_functions import returnNone

# Very important, get the directory that the user wants to run commands in
cwd = os.getcwd()


def incrementFilename(path):
    fn, extension = os.path.splitext(path)

    n = 1
    yield fn + extension
    for n in itertools.count(start=1, step=1):
        yield '%s-%d%s' % (fn, n, extension)


def getUnused(path):
    useable_file = ""
    for filename in incrementFilename(path):
        if not os.path.isfile(filename):
            useable_file = filename
            break

    return useable_file


def createPost():
    if sys.version_info < (3, 0):
        subtype = raw_input("Post Subtype: ")
        title = raw_input("Post Title: ")
        subtitle = raw_input("Post Subtitle: ")
        author = raw_input("Post Author: ")
        date = raw_input("Post Date: ")
        tags = raw_input("Post Tags: ")
        categories = raw_input("Post Categories: ")
        image = raw_input("Post Image: ")
        content = raw_input("Post Content: ")
    else:
        subtype = input("Post Subtype: ")
        title = input("Post Title: ")
        subtitle = input("Post Subtitle: ")
        author = input("Post Author: ")
        date = input("Post Date: ")
        tags = input("Post Tags: ")
        categories = input("Post Categories: ")
        image = input("Post Image: ")
        content = input("Post Content: ")

    filename = getUnused(os.path.join(
        cwd, "content", "posts", title.replace(" ", "_").replace("?", "").replace("!", "") + ".html"))

    with open(filename, 'w') as wfile:
        wfile.write("---\n")
        wfile.write("type: post\n")
        wfile.write("subtype: " + returnNone(subtype) + "\n")
        wfile.write("title: " + title + "\n")
        wfile.write("subtitle: " + subtitle + "\n")
        wfile.write("author: " + author + "\n")
        wfile.write("date: " + date + "\n")
        wfile.write("tags: " + tags + "\n")
        wfile.write("categories: " + categories + "\n")
        wfile.write("image: " + image + "\n")
        wfile.write("---\n")
        wfile.write(content)


def createPage():
    print("Creating a page!")
