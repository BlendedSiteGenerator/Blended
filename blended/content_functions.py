import itertools
import os
import sys

import mammoth
import markdown
import pyjade
import textile
from docutils.core import publish_parts

from .app_functions import createFolder, returnNone

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

    createFolder(os.path.join(cwd, "content", "posts"))
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
    if sys.version_info < (3, 0):
        subtype = raw_input("Page Subtype: ")
        title = raw_input("Page Title: ")
        subtitle = raw_input("Page Subtitle: ")
        image = raw_input("Page Image: ")
        content = raw_input("Page Content: ")
    else:
        subtype = input("Page Subtype: ")
        title = input("Page Title: ")
        subtitle = input("Page Subtitle: ")
        image = input("Page Image: ")
        content = input("Page Content: ")

    filename = getUnused(os.path.join(
        cwd, "content", "pages", title.replace(" ", "_").replace("?", "").replace("!", "") + ".html"))

    createFolder(os.path.join(cwd, "content", "pages"))
    with open(filename, 'w') as wfile:
        wfile.write("---\n")
        wfile.write("type: page\n")
        wfile.write("subtype: " + returnNone(subtype) + "\n")
        wfile.write("title: " + title + "\n")
        wfile.write("subtitle: " + subtitle + "\n")
        wfile.write("image: " + image + "\n")
        wfile.write("---\n")
        wfile.write(content)


def convertContent(content, filename):
    if filename.endswith(".html"):
        return content
    elif filename.endswith(".txt"):
        return content
    elif filename.endswith(".md"):
        return markdown.markdown(content, ['markdown.extensions.extra'])
    elif filename.endswith(".tile"):
        return textile.textile(content)
    elif filename.endswith(".docx"):
        return mammoth.convert_to_html(content)
    elif filename.endswith(".jade"):
        return pyjade.simple_convert(content)
    elif filename.endswith(".rst"):
        return publish_parts(content, writer_name='html')['html_body']
    else:
        print(filename + " is not a supported file type! HTML, TXT, MD, TILE, DOCX, JADE, and RST are supported.")
