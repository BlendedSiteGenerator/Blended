import os
import sys
import shutil
import importlib
import frontmatter
from term_colors import term_colors

# Very important, get the directory that the user wants to run commands in
cwd = os.getcwd()


def build_site():
    config_file_dir = os.path.join(cwd, "config.py")
    if not os.path.exists(config_file_dir):
        sys.exit(term_colors.FAIL +
                 "ERROR: There dosen't seem to be a configuration file. Have you run the init command?" + term_colors.ENDC)
    else:
        sys.path.insert(0, cwd)
        try:
            from config import site_title, theme
        except:
            sys.exit(term_colors.FAIL + "ERROR: Some of the crucial configuration values could not be found! Maybe your config.py is too old. Run 'blended init' to fix." + term_colors.ENDC)
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
            print(term_colors.WARNING + "WARNING: Some of the optional configuration values could not be found! Maybe your config.py is too old. Run 'blended init' to fix.\n" + term_colors.ENDC)

    if site_title.strip() == "":
        sys.exit(term_colors.FAIL +
                 "ERROR: You must have a site_title!" + term_colors.ENDC)
    elif theme.strip() == "":
        sys.exit(term_colors.FAIL +
                 "ERROR: You must have a theme!" + term_colors.ENDC)
