import os
import sys
import shutil
import importlib
import frontmatter

# Very important, get the directory that the user wants to run commands in
cwd = os.getcwd()


def build_site():
    config_file_dir = os.path.join(cwd, "config.py")
    if not os.path.exists(config_file_dir):
        sys.exit(
            "There dosen't seem to be a configuration file. Have you run the init command?")
    else:
        sys.path.insert(0, cwd)
        try:
            from config import site_title, theme
        except:
            sys.exit(
                "ERROR: Some of the crucial configuration values could not be found! Maybe your config.py is too old. Run 'blended init' to fix.")
        try:
            from config import site_tagline, site_language, date_format, time_format, permalink_format, blog_list_posts, blog_list_post_item, front_page, plugins
        except:
            site_tagline = ""
            site_language = "en-US"
            date_format = "F j, Y"
            time_format = "g:i a"
            permalink_format = "day_and_name"
            blog_list_posts = 10
            blog_list_post_item = "full_text"
            front_page = "latest_posts"
            plugins = []
            print("WARNING: Some of the optional configuration values could not be found! Maybe your config.py is too old. Run 'blended init' to fix.\n")
