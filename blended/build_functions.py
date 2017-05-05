import json
import os
import shutil
import sys

import click
import frontmatter
from jinja2 import Environment, PackageLoader, select_autoescape

from .app_functions import createFolder, replaceFolder

# Very important, get the directory that the user wants to run commands in
cwd = os.getcwd()


def buildFiles():
    config_file_dir = os.path.join(cwd, "config.json")
    if not os.path.exists(config_file_dir):
        sys.exit(
            "There dosen't seem to be a configuration file. Have you run the init command?")
    else:
        with open(config_file_dir) as config_file:
            config = json.load(config_file)

    generateBuildDir(site_theme=config['theme'])

    root_templates_folder = os.path.join(
        cwd, "_themes", config['theme'])

    env = Environment(
        loader=PackageLoader('blended', root_templates_folder)
    )

    env.globals['siteinfo'] = config

    menus = {}
    for root, dirs, files in os.walk(os.path.join(cwd, "_menus")):
        for filename in files:
            if not filename.startswith("_"):
                with open(os.path.join(root, filename)) as f:
                    menu = json.load(f)
                    menus[filename.replace(".json", "")] = menu

    env.globals['menus'] = menus

    blog_posts = []
    for root, dirs, files in os.walk(cwd):
        dirs[:] = [d for d in dirs if "_" not in d and d != "build"]
        for filename in files:
            if not filename.startswith("_") and filename != "config.json":
                with open(os.path.join(root, filename)) as f:
                    filei = frontmatter.load(f)
                    if filei['type'] == "post":
                        date = str(filei['date'])
                        blog_posts.append(filei)

                        if os.path.exists(os.path.join(cwd, "_themes", config['theme'], filei['subtype'] + ".html")):
                            template = env.get_template(
                                filei['subtype'] + ".html")
                        elif os.path.exists(os.path.join(cwd, "_themes", config['theme'], "post.html")):
                            template = env.get_template('post.html')
                        else:
                            template = env.get_template('index.html')

                        createFolder(os.path.join(cwd, "build", date.split(
                            "-")[0], date.split("-")[1], date.split("-")[2]))
                        with open(os.path.join(cwd, "build", date.split("-")[0], date.split("-")[1], date.split("-")[2], filei['title'].replace(" ", "_").replace("?", "") + ".html"), 'w') as output:
                            output.write(template.render(
                                post=filei, root="../../../", is_home=False, is_page=False, is_post=True))

                    elif filei['type'] == "page":
                        date = str(filei['date'])

                        if os.path.exists(os.path.join(cwd, "_themes", config['theme'], filei['subtype'] + ".html")):
                            template = env.get_template(
                                filei['subtype'] + ".html")
                        elif os.path.exists(os.path.join(cwd, "_themes", config['theme'], "page.html")):
                            template = env.get_template('page.html')
                        else:
                            template = env.get_template('index.html')

                        createFolder(os.path.join(cwd, "build"))
                        with open(os.path.join(cwd, "build", filei['title'].replace(" ", "_").replace("?", "") + ".html"), 'w') as output:
                            output.write(template.render(
                                page=filei, root="", is_home=False, is_page=True, is_post=False))

    if os.path.exists(os.path.join(cwd, "_themes", config['theme'], "posts.html")):
        template = env.get_template('posts.html')
    else:
        template = env.get_template('index.html')

    with open(os.path.join(cwd, "build", "index.html"), 'w') as output:
        output.write(template.render(
            posts=sorted(blog_posts, key=lambda post: post['date'], reverse=True), root="", is_home=True, is_page=False, is_post=False))


def generateBuildDir(site_theme):
    createFolder(os.path.join(cwd, "build"))

    if os.path.exists(os.path.join(cwd, "_themes", site_theme, "assets")):
        if os.path.exists(os.path.join(cwd, "build", "assets")):
            shutil.rmtree(os.path.join(cwd, "build", "assets"))
        shutil.copytree(os.path.join(cwd, "_themes", site_theme, "assets"),
                        os.path.join(cwd, "build", "assets"))

    if os.path.exists(os.path.join(cwd, "_media")):
        if os.path.exists(os.path.join(cwd, "build", "media")):
            shutil.rmtree(os.path.join(cwd, "build", "media"))
        shutil.copytree(os.path.join(cwd, "_media"),
                        os.path.join(cwd, "build", "media"))
