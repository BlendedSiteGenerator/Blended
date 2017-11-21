import os
import sys

from .config_functions import checkConfig
from .content_functions import getUnused, parseXML

# Very important, get the directory that the user wants to run commands in
cwd = os.getcwd()


def importWordPress(filepath):
    """Import posts from WordPress"""
    if not checkConfig():
        sys.exit(
            "There dosen't seem to be a configuration file. Have you run the init command?")

    wp = parseXML(filepath)

    for item in wp.rss.channel.item:
        with open(getUnused(os.path.join(cwd, "content", "posts", item.title.cdata.replace(" ", "_").replace("?", "").replace("!", "") + ".html")), 'w') as wfile:
            wfile.write("---\n")
            wfile.write("type: post\n")
            wfile.write("subtype: NONE\n")
            wfile.write("title: " + item.title.cdata + "\n")
            wfile.write("subtitle: \n")
            wfile.write("author: " + item.dc_creator.cdata + "\n")
            wfile.write("date: " + item.wp_post_date.cdata[0:10] + "\n")
            wfile.write("tags: \n")
            wfile.write("categories: Uncategorized\n")
            wfile.write("image: \n")
            wfile.write("custom_path: \n")
            wfile.write("---\n")
            wfile.write(item.content_encoded.cdata.strip())
