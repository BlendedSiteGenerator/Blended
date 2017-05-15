import json
import os
import shutil
import sys
import time

import frontmatter
from jinja2 import Environment, PackageLoader, select_autoescape, Template

from .app_functions import createFolder, getVersion, replaceFolder
from .content_functions import convertContent

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

    if not os.path.exists(os.path.join(cwd, "themes", config['theme'], "index.html")):
        sys.exit("The theme you have chosen does not have an index.html file!")

    generateBuildDir(site_theme=config['theme'])

    root_templates_folder = os.path.join(
        cwd, "themes", config['theme'])

    env = Environment(
        loader=PackageLoader('blended', root_templates_folder)
    )

    env.globals['siteinfo'] = config

    buildinfo = {"date": time.strftime("%Y-%m-%d"),
                 "day": time.strftime("%d"),
                 "month": time.strftime("%m"),
                 "year": time.strftime("%Y"),
                 "time24": time.strftime("%H:%M:%S"),
                 "time12": time.strftime("%I:%M:%S %p"),
                 "blended_version": getVersion()
                 }
    env.globals['buildinfo'] = buildinfo

    # Authors
    authors_file = os.path.join(cwd, "data", "authors.json")
    if os.path.exists(authors_file):
        with open(authors_file) as f:
            authors = json.load(f)
    else:
        authors = []

    env.globals['authors'] = authors

    header = "<meta name=\"generator\" content=\"Blended v" + getVersion() + "\" />"
    env.globals['blended_header'] = header

    menus = {}
    for root, dirs, files in os.walk(os.path.join(cwd, "data", "menus")):
        for filename in files:
            if not filename.startswith("_"):
                with open(os.path.join(root, filename)) as f:
                    menu = json.load(f)
                    menus[filename.replace(".json", "")] = menu

    env.globals['menus'] = menus

    def render(template, values):
         prev = template.render(**values)
         while True:
             curr = Template(prev).render(siteinfo=config, menus=menus, blended_header=header, authors=authors, buildinfo=buildinfo, **values)
             if curr != prev:
                 prev = curr
             else:
                 return curr

    posts = []
    pages = []
    tags = []
    categories = []
    if config['build_posts'] or config['build_pages']:
        for root, dirs, files in os.walk(os.path.join(cwd, "content")):
            dirs[:] = [d for d in dirs if "_" not in d]
            for filename in files:
                if not filename.startswith("_"):
                    with open(os.path.join(root, filename)) as f:
                        filei = frontmatter.load(f)
                        if filei['type'] == "post":
                            date = str(filei['date'])
                            permalink = date.split("-")[0] + "/" + date.split("-")[1] + "/" + date.split(
                                "-")[2] + "/" + filei['title'].replace(" ", "_").replace("?", "").replace("!", "") + ".html"
                            filei['permalink'] = permalink
                            filei.content = convertContent(
                                filei.content, filename)
                            tags.append(filei['tags'].split(", "))
                            categories.append(filei['categories'].split(", "))
                            posts.append(filei)

                        elif filei['type'] == "page":
                            filei.content = convertContent(
                                filei.content, filename)
                            pages.append(filei)

    if config['build_posts']:
        for post in posts:
            date = str(post['date'])
            if os.path.exists(os.path.join(cwd, "themes", config['theme'], post['subtype'] + ".html")):
                template = env.get_template(
                    post['subtype'] + ".html")
            elif os.path.exists(os.path.join(cwd, "themes", config['theme'], "post.html")):
                template = env.get_template('post.html')
            elif os.path.exists(os.path.join(cwd, "themes", config['theme'], "single.html")):
                template = env.get_template('single.html')
            else:
                template = env.get_template('index.html')

            if post['custom_path']:
                pathsk = post['custom_path'].split("/")
                folder = os.path.join(cwd, "build", *pathsk)
                title = post['title'].replace(" ", "_").replace("?", "").replace("!", "") + ".html"
                ffile = os.path.join(cwd, "build", post['custom_path'], title)
                root = ""
                for item in pathsk:
                    root = root + "../"
            else:
                folder = os.path.join(cwd, "build", date.split("-")[0], date.split("-")[1], date.split("-")[2])
                ffile = os.path.join(cwd, "build", date.split("-")[0], date.split("-")[1], date.split("-")[2], post['title'].replace(" ", "_").replace("?", "").replace("!", "") + ".html")
                root = "../../../"

            createFolder(folder)
            with open(ffile, 'w') as output:
                output.write(render(template, dict(
                    content=post, tags=tags, categories=categories, root=root, is_home=False, is_page=False, is_post=True, is_author=False)))

    if config['build_pages']:
        for page in pages:
            if os.path.exists(os.path.join(cwd, "themes", config['theme'], page['subtype'] + ".html")):
                template = env.get_template(
                    page['subtype'] + ".html")
            elif os.path.exists(os.path.join(cwd, "themes", config['theme'], "page.html")):
                template = env.get_template('page.html')
            elif os.path.exists(os.path.join(cwd, "themes", config['theme'], "single.html")):
                template = env.get_template('single.html')
            else:
                template = env.get_template('index.html')

            if page['custom_path']:
                pathsk = page['custom_path'].split("/")
                createFolder(os.path.join(cwd, "build", page['custom_path']))
                ffile = os.path.join(cwd, "build", page['custom_path'], page['title'].replace(" ", "_").replace("?", "").replace("!", "") + ".html")
                root = ""
                for item in pathsk:
                    root = root + "../"
            else:
                ffile = os.path.join(cwd, "build", page['title'].replace(" ", "_").replace("?", "").replace("!", "") + ".html")
                root = ""

            with open(ffile, 'w') as output:
                output.write(render(template, dict(
                    content=page,
                    posts=sorted(posts, key=lambda post: post['date'], reverse=True), tags=tags, categories=categories, root=root, is_home=False, is_page=True, is_post=False, is_author=False)))

    if config['build_home']:
        if os.path.exists(os.path.join(cwd, "themes", config['theme'], "posts.html")):
            template = env.get_template('posts.html')
        elif os.path.exists(os.path.join(cwd, "themes", config['theme'], "home.html")):
            template = env.get_template('home.html')
        else:
            template = env.get_template('index.html')

        with open(os.path.join(cwd, "build", "index.html"), 'w') as output:
            output.write(render(template, dict(
                posts=sorted(posts, key=lambda post: post['date'], reverse=True), tags=tags, categories=categories, root="", is_home=True, is_page=False, is_post=False, is_author=False)))

    if config['build_authors']:
        for author in authors:
            if os.path.exists(os.path.join(cwd, "themes", config['theme'], "author.html")):
                template = env.get_template("author.html")
            elif os.path.exists(os.path.join(cwd, "themes", config['theme'], "single.html")):
                template = env.get_template('single.html')
            else:
                template = env.get_template('index.html')

            createFolder(os.path.join(cwd, "build", "authors"))
            with open(os.path.join(cwd, "build", "authors", author.replace(" ", "_").replace("?", "").replace("!", "") + ".html"), 'w') as output:
                output.write(render(template, dict(
                    content={"title": author}, author=authors[author], tags=tags, categories=categories, root="../", is_home=False, is_page=True, is_post=False, is_author=True)))


def generateBuildDir(site_theme):
    createFolder(os.path.join(cwd, "build"))

    if os.path.exists(os.path.join(cwd, "themes", site_theme, "assets")):
        if os.path.exists(os.path.join(cwd, "build", "assets")):
            shutil.rmtree(os.path.join(cwd, "build", "assets"))
        shutil.copytree(os.path.join(cwd, "themes", site_theme, "assets"),
                        os.path.join(cwd, "build", "assets"))

    if os.path.exists(os.path.join(cwd, "media")):
        if os.path.exists(os.path.join(cwd, "build", "media")):
            shutil.rmtree(os.path.join(cwd, "build", "media"))
        shutil.copytree(os.path.join(cwd, "media"),
                        os.path.join(cwd, "build", "media"))
