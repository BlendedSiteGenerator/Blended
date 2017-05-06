import json
import os
import sys
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
        sys.exit(
            "There dosen't seem to be a theme settings file!")
    else:
        with open(theme_config_file_dir) as theme_config_file:
            theme_config = json.load(theme_config_file)

    config['theme_params'] = theme_config

    print(json.dumps(OrderedDict([("blended_version", config['blended_version']), ("title", config['title']), ("subtitle", config['subtitle']), ("description", config['description']), ("language", config['language']), ("theme", config['theme']),
                                  ("build_home", config['build_home']), ("build_posts", config['build_home']), ("build_pages", config['build_pages']), ("build_authors", config['build_authors']), ("theme_params", config['theme_params'])]), indent=4))
