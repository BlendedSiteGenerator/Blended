import os
import sys
import shutil
import importlib
import frontmatter
from dateutil import parser as date_parser
from term_colors import term_colors
from functions import force_exist

# Very important, get the directory that the user wants to run commands in
cwd = os.getcwd()


def get_content(filepath):
    output = {}
    options = frontmatter.load(filepath)

    if filepath.endswith(".html"):
        fformat = "html"
    elif filepath.endswith(".md") or filepath.endswith(".markdown"):
        fformat = "markdown"
    else:
        sys.exit(term_colors.FAIL + "The file format of " + filepath +
                 " is not recognized! It must be HTML (.html) or Markdown (.md, .markdown)." + term_colors.ENDC)

    if options['type'] == "post":
        output = {"format": fformat, "title": options['title'], "author": options['author'], "categories": options['categories'], "tags": options['tags'],
                  "image": options['image'], "date": date_parser.parse(options['date']).date(), "type": options['type'], "content": options.content}
    elif options['type'] == "page":
        output = {"format": fformat, "title": options['title'], "author": options['author'], "image": options['image'],
                  "date": date_parser.parse(options['date']).date(), "type": options['type'], "content": options.content}
    else:
        sys.exit(term_colors.FAIL +
                 "That content type is not recognized!" + term_colors.ENDC)

    return output


def build_site(outdir):
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

    header_file = os.path.join(cwd, "includes", "themes", theme, "header.html")
    footer_file = os.path.join(cwd, "includes", "themes", theme, "footer.html")
    post_file = os.path.join(cwd, "includes", "themes", theme, "post.html")
    force_exist([post_file, header_file, footer_file], "template")

    header_content = open(header_file).read()
    print(header_content)

    for root, dirs, files in os.walk(os.path.join(cwd, "content")):
        for filename in files:
            content = get_content(os.path.join(root, filename))
            template_file = os.path.join(
                cwd, "includes", "themes", theme, content['type'] + ".html")
            if not os.path.exists(template_file):
                print(term_colors.WARNING +
                      "WARNING: The " + content['type'] + ".html template does not exist. Using post.html instead." + term_colors.ENDC)
