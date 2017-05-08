import json
import os
import sys
import urllib
import zipfile
from collections import OrderedDict

# Very important, get the directory that the user wants to run commands in
cwd = os.getcwd()


def setupTheme(theme):
    config_file_dir = os.path.join(cwd, "config.json")
    if not os.path.exists(config_file_dir):
        sys.exit(
            "There dosen't seem to be a configuration file. Have you run the init command?")
    else:
        with open(config_file_dir) as config_file:
            config = json.load(config_file)

    theme_config_file_dir = os.path.join(cwd, "themes", theme, "settings.json")
    if not os.path.exists(theme_config_file_dir):
        theme_config = {}
    else:
        with open(theme_config_file_dir) as theme_config_file:
            theme_config = json.load(theme_config_file)

    config['theme'] = theme
    config['theme_params'] = theme_config

    with open(config_file_dir, 'w') as config_file:
        config_file.write(json.dumps(OrderedDict([("blended_version", config['blended_version']),
                                                  ("title", config['title']),
                                                  ("subtitle",
                                                   config['subtitle']),
                                                  ("language",
                                                   config['language']),
                                                  ("theme", config['theme']),
                                                  ("build_home",
                                                   config['build_home']),
                                                  ("build_posts",
                                                   config['build_posts']),
                                                  ("build_pages",
                                                   config['build_pages']),
                                                  ("build_authors",
                                                   config['build_authors']),
                                                  ("theme_params", config['theme_params'])]), indent=4))


def downloadTheme(theme):
    thedir = os.path.join(cwd, "themes")
    theurl = "https://github.com/BlendedSiteGenerator/BlendedThemes/blob/master/" + \
        theme + ".zip?raw=true"
    name = os.path.join(thedir, 'temp.zip')
    try:
        name = urllib.urlretrieve(theurl, name)
        name = os.path.join(thedir, 'temp.zip')
    except IOError, e:
        print "Can't retrieve %r to %r: %s" % (theurl, thedir, e)
        return
    try:
        z = zipfile.ZipFile(name)
    except zipfile.error, e:
        print "Bad zipfile (from %r): %s" % (theurl, e)
        return
    z.extractall(thedir)
    z.close()
    os.remove(name)
