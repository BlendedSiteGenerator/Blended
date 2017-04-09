# encoding=utf8
import os
import os.path
import sys
from sys import platform
import shutil
import fileinput
import webbrowser
import fileinput
from datetime import datetime
import click
from random import randint
import pkg_resources
import time
from ftplib import FTP, error_perm
import markdown
import textile
from docutils.core import publish_parts
import mammoth
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import importlib
import sass
import pyjade
import lesscpy
import subprocess
from six import StringIO
from stylus import Stylus
import coffeescript
from jsmin import jsmin
from cssmin import cssmin
import pip
from .functions import *

# Very important, get the directory that the user wants to run commands in
cwd = os.getcwd()

try:
    app_version = pkg_resources.require("blended")[0].version
    app_version = app_version[:3]
except:
    app_version = "NOTSET"
    print("WARNING: app_version not set.\n")


@click.group()
def cli():
    """Blended: Static Website Generator"""


@cli.command('info', short_help='Show info about Blended and the current project.')
def version():
    """Prints info about Blended"""

    print("You are running Blended v" + app_version)
    print("The current working directory is " + cwd)


@cli.command('install-template', short_help='Install a Blended template from GitHub')
@click.option('--username', prompt='GitHub username/organization',
              help='The GitHub username/organization.')
@click.option('--repo', prompt='GitHub repository',
              help='The GitHub repository name.')
def install_template(username, repo):
    """Installs a Blended template from GitHub"""
    print("Installing template from " + username + "/" + repo)

    dpath = os.path.join(cwd, "templates")
    getunzipped(username, repo, dpath)


@cli.command('import-wp', short_help='Import a site from WordPress')
@click.option('--filepath', prompt='WordPress export file', help='Which file holds the exported data from WordPress')
def install_template(filepath):
    """Imports A WordPress export and converts it to a Blended site"""

    print("\nBlended: Static Website Generator -\n")

    checkConfig()
    print("Importing from WordPress...")

    wp = parseXML(filepath)

    wname = wp.rss.channel.title.cdata
    wdesc = wp.rss.channel.description.cdata
    wlan = wp.rss.channel.language.cdata
    wurl = wp.rss.channel.link.cdata
    aname = wp.rss.channel.wp_author.wp_author_display_name.cdata.strip()

    createBlendedFolders()

    # Populate the configuration file
    createConfig(app_version=app_version, wname=wname,
                 wdesc=wdesc, wlan=wlan, wurl=wurl, aname=aname)

    for item in wp.rss.channel.item:
        with open(os.path.join(cwd, "content", item.title.cdata.replace(" ", "_") + ".html"), 'w') as file:
            file.write(item.content_encoded.cdata.strip())

    print("\nYour website has been imported from WordPress.")


@cli.command('import-blogger', short_help='Import a site from Blogger')
@click.option('--filepath', prompt='Blogger export file', help='Which file holds the exported data from Blogger')
def install_template(filepath):
    """Imports A Blogger export and converts it to a Blended site"""

    print("\nBlended: Static Website Generator -\n")

    checkConfig()
    print("Importing from Blogger...")

    blogger = parseXML(filepath)

    wname = blogger.feed.title.cdata
    aname = blogger.feed.author.name.cdata.strip()

    createBlendedFolders()

    # Populate the configuration file
    createConfig(app_version=app_version, wname=wname, aname=aname)

    for entry in blogger.feed.entry:
        if "post" in entry.id.cdata:
            with open(os.path.join(cwd, "content", entry.title.cdata.replace(" ", "_") + ".html"), 'w') as file:
                file.write(entry.content.cdata.strip())

    print("\nYour website has been imported from Blogger.")


@cli.command('install-plugin', short_help='Install a Blended plugin from GitHub')
@click.option('--username', prompt='GitHub username/organization',
              help='The GitHub username/organization.')
@click.option('--repo', prompt='GitHub repository',
              help='The GitHub repository name.')
def install_plugin(username, repo):
    """Installs a Blended plugin from GitHub"""
    print("Installing plugin from " + username + "/" + repo)

    pip.main(['install', '-U', "git+git://github.com/" +
              username + "/" + repo + ".git"])


@cli.command('init', short_help='Initiate a new website')
def init():
    """Initiates a new website"""

    print("Blended: Static Website Generator -\n")

    checkConfig()

    if (sys.version_info > (3, 0)):
        wname = input("Website Name: ")
        wdesc = input("Website Description: ")
        wlan = input("Website Language: ")
        wlic = input("Website License: ")
        aname = input("Author(s) Name(s): ")
    else:
        wname = raw_input("Website Name: ")
        wdesc = raw_input("Website Description: ")
        wlan = raw_input("Website Language: ")
        wlic = raw_input("Website License: ")
        aname = raw_input("Author(s) Name(s): ")

    createBlendedFolders()

    # Populate the configuration file
    createConfig(app_version=app_version, wname=wname,
                 wdesc=wdesc, wlic=wlic, wlan=wlan, aname=aname)

    print("\nThe required files for your website have been generated.")


def placeFiles(ftp, path):
    for name in os.listdir(path):
        if name != "config.py" and name != "config.pyc" and name != "templates" and name != "content":
            localpath = os.path.join(path, name)
            if os.path.isfile(localpath):
                print("STOR", name, localpath)
                ftp.storbinary('STOR ' + name, open(localpath, 'rb'))
            elif os.path.isdir(localpath):
                print("MKD", name)

                try:
                    ftp.mkd(name)

                # ignore "directory already exists"
                except error_perm as e:
                    if not e.args[0].startswith('550'):
                        raise

                print("CWD", name)
                ftp.cwd(name)
                placeFiles(ftp, localpath)
                print("CWD", "..")
                ftp.cwd("..")


@cli.command('ftp', short_help='Upload the files via ftp')
@click.option('--outdir', default="build", help='Choose which folder the built files are in. Default is `build`.')
def ftp(outdir):
    """Upload the built website to FTP"""
    print("Uploading the files in the " + outdir + "/ directory!\n")

    # Make sure there is actually a configuration file
    config_file_dir = os.path.join(cwd, "config.py")
    if not os.path.exists(config_file_dir):
        sys.exit(
            "There dosen't seem to be a configuration file. Have you run the init command?")
    else:
        sys.path.insert(0, cwd)
        try:
            from config import ftp_server, ftp_username, ftp_password, ftp_port, ftp_upload_path
        except:
            sys.exit(
                "The FTP settings could not be found. Maybe your config file is too old. Re-run 'blended init' to fix it.")

    server = ftp_server
    username = ftp_username
    password = ftp_password
    port = ftp_port

    ftp = FTP()
    ftp.connect(server, port)
    ftp.login(username, password)
    filenameCV = os.path.join(cwd, outdir)

    try:
        ftp.cwd(ftp_upload_path)
        placeFiles(ftp, filenameCV)
    except:
        ftp.quit()
        sys.exit("Files not able to be uploaded! Are you sure the directory exists?")

    ftp.quit()

    print("\nFTP Done!")


@cli.command('clean', short_help='Remove the build folder')
@click.option('--outdir', default="build", help='Choose which folder the built files are in. Default is `build`.')
def clean(outdir):
    """Removes all built files"""
    print("Removing the built files!")

    # Remove the  build folder
    build_dir = os.path.join(cwd, outdir)
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)


@cli.command('zip', short_help='Package the build folder into a zip file')
@click.option('--outdir', default="build", help='Choose which folder the built files are in. Default is `build`.')
def zip(outdir):
    """Packages the build folder into a zip"""
    print("Zipping the built files!")

    config_file_dir = os.path.join(cwd, "config.py")
    if not os.path.exists(config_file_dir):
        sys.exit(
            "There dosen't seem to be a configuration file. Have you run the init command?")
    else:
        sys.path.insert(0, cwd)
        try:
            from config import website_name
        except:
            sys.exit(
                "Some of the configuration values could not be found! Maybe your config.py is too old. Run 'blended init' to fix.")

    # Remove the  build folder
    build_dir = os.path.join(cwd, outdir)
    zip_dir = os.path.join(cwd, website_name + "-build-" +
                           str(datetime.now().date()))
    if os.path.exists(build_dir):
        shutil.make_archive(zip_dir, 'zip', build_dir)
    else:
        print("The " + outdir +
              "/ folder could not be found! Have you run 'blended build' yet?")


@cli.command('purge', short_help='Purge all the files created by Blended')
def purge():
    """Removes all files generated by Blended"""
    print("Purging the Blended files!")

    # Remove the templates folder
    templ_dir = os.path.join(cwd, "templates")
    if os.path.exists(templ_dir):
        shutil.rmtree(templ_dir)

    # Remove the content folder
    cont_dir = os.path.join(cwd, "content")
    if os.path.exists(cont_dir):
        shutil.rmtree(cont_dir)

    # Remove the  build folder
    build_dir = os.path.join(cwd, "build")
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)

    # Remove config.py
    config_file_dir = os.path.join(cwd, "config.py")
    if os.path.exists(config_file_dir):
        os.remove(config_file_dir)

    # Remove config.pyc
    config2_file_dir = os.path.join(cwd, "config.pyc")
    if os.path.exists(config2_file_dir):
        os.remove(config2_file_dir)

    # Remove config.py
    config3_file_dir = os.path.join(cwd, "config.py.oldbak")
    if os.path.exists(config3_file_dir):
        os.remove(config3_file_dir)


def convert_text(filename):
    text_content = open(filename, "r")
    if ".md" in filename:
        text_cont1 = "\n" + markdown.markdown(text_content.read()) + "\n"
    elif ".docx" in filename:
        with open(os.path.join(cwd, "content", filename), "rb") as docx_file:
            result = mammoth.convert_to_html(docx_file)
            final_docx_html = result.value
        text_cont1 = "\n" + final_docx_html + "\n"
    elif ".tile" in filename:
        text_cont1 = "\n" + textile.textile(text_content.read()) + "\n"
    elif ".jade" in filename:
        text_cont1 = "\n" + pyjade.simple_convert(text_content.read()) + "\n"
    elif ".rst" in filename:
        text_cont1 = "\n" + \
            publish_parts(text_content.read(), writer_name='html')[
                'html_body'] + "\n"
    elif ".html" in filename:
        text_cont1 = text_content.read()
    elif ".txt" in filename:
        text_cont1 = text_content.read()
    else:
        print(filename + " is not a valid file type!")
        text_cont1 = "NULL"

    return text_cont1 + "\n\n"


def build_files(outdir):
    # Make sure there is actually a configuration file
    config_file_dir = os.path.join(cwd, "config.py")
    if not os.path.exists(config_file_dir):
        sys.exit(
            "There dosen't seem to be a configuration file. Have you run the init command?")
    else:
        sys.path.insert(0, cwd)
        try:
            from config import website_name, website_description, website_language, home_page_list
        except:
            sys.exit(
                "ERROR: Some of the crucial configuration values could not be found! Maybe your config.py is too old. Run 'blended init' to fix.")
        try:
            from config import website_description_long, website_license, website_url, author_name, author_bio, plugins, minify_css, minify_js, custom_variables
        except:
            website_description_long = ""
            website_license = ""
            website_url = ""
            author_name = ""
            author_bio = ""
            plugins = []
            custom_variables = {}
            minify_css = False
            minify_js = False
            print("WARNING: Some of the optional configuration values could not be found! Maybe your config.py is too old. Run 'blended init' to fix.\n")

    # Create the build folder
    build_dir = os.path.join(cwd, outdir)
    if "." not in outdir and ".." not in outdir and "..." not in outdir and "...." not in outdir and "....." not in outdir:
        replace_folder(build_dir)

    # Make sure there is actually a header template file
    header_file_dir = os.path.join(cwd, "templates", "header.html")
    if not os.path.exists(header_file_dir):
        sys.exit(
            "There dosen't seem to be a header template file. You need one to generate.")

    # Make sure there is actually a footer template file
    footer_file_dir = os.path.join(cwd, "templates", "footer.html")
    if not os.path.exists(footer_file_dir):
        sys.exit(
            "There dosen't seem to be a footer template file. You need one to generate.")

    # Open the header and footer files for reading
    header_file = open(header_file_dir, "r")
    footer_file = open(footer_file_dir, "r")

    # Create the HTML page listing
    page_list_item_file = os.path.join(cwd, "templates", "page_list_item.html")
    if not os.path.exists(page_list_item_file):
        page_list = '<ul class="page-list">\n'
        for root, dirs, files in os.walk(os.path.join(cwd, "content")):
            for filename in files:
                top = os.path.dirname(os.path.join(root, filename))
                top2 = top.replace(os.path.join(cwd, "content"), "", 1)
                if platform != "win32":
                    subfolder = top2.replace("/", "", 1)
                else:
                    subfolder = top2.replace("\\", "", 1)

                if subfolder == "":
                    subfolder_link = ""
                else:
                    subfolder_link = subfolder + "/"
                file_modified = time.ctime(
                    os.path.getmtime(os.path.join(root, filename)))
                newFilename = get_html_filename(filename)
                newFilename2 = get_html_clear_filename(filename)
                page_list = page_list + '<li class="page-list-item"><a href="' + subfolder_link + newFilename + \
                    '">' + newFilename2 + '</a><span class="page-list-item-time"> - ' + \
                    str(file_modified) + '</span></li>\n'
        page_list = page_list + '</ul>'
    else:
        with open(page_list_item_file, 'r') as f:
            page_list_item = f.read()

        page_list = ""
        for root, dirs, files in os.walk(os.path.join(cwd, "content")):
            dirs[:] = [d for d in dirs if "_" not in d]
            for filename in files:
                p_content = convert_text(os.path.join(root, filename))
                top = os.path.dirname(os.path.join(root, filename))
                top2 = top.replace(os.path.join(cwd, "content"), "", 1)
                if platform != "win32":
                    subfolder = top2.replace("/", "", 1)
                else:
                    subfolder = top2.replace("\\", "", 1)

                if subfolder == "":
                    subfolder_link = ""
                else:
                    subfolder_link = subfolder + "/"
                file_modified = time.ctime(
                    os.path.getmtime(os.path.join(root, filename)))
                file_modified_day = str(datetime.strptime(
                    file_modified, "%a %b %d %H:%M:%S %Y"))[5:7]
                file_modified_year = str(datetime.strptime(
                    file_modified, "%a %b %d %H:%M:%S %Y"))[:4]
                file_modified_month = str(datetime.strptime(
                    file_modified, "%a %b %d %H:%M:%S %Y"))[8:10]
                newFilename = get_html_filename(filename)
                newFilename2 = get_html_clear_filename(filename)

                page_list = page_list + page_list_item.replace("{path}", subfolder_link + newFilename).replace("{name}", newFilename2).replace(
                    "{date}", str(file_modified)).replace("{content}", p_content).replace("{content_short}", p_content[:250] + "...").replace("{day}", file_modified_day).replace("{month}", file_modified_month).replace("{year}", file_modified_year)

    if home_page_list == "yes" or home_page_list:
        # Open the home page file (index.html) for writing
        home_working_file = open(os.path.join(cwd, outdir, "index.html"), "w")

        home_working_file.write(header_file.read())

        # Make sure there is actually a home page template file
        home_templ_dir = os.path.join(cwd, "templates", "home_page.html")
        if os.path.exists(home_templ_dir):
            home_templ_file = open(home_templ_dir, "r")
            home_working_file.write(home_templ_file.read())
        else:
            print("\nNo home page template file found. Writing page list to index.html")
            home_working_file.write(page_list)

        home_working_file.write(footer_file.read())

        home_working_file.close()

    for root, dirs, files in os.walk(os.path.join(cwd, "content")):
        dirs[:] = [d for d in dirs if "_" not in d]
        for filename in files:
            if not filename.startswith("_"):
                header_file = open(header_file_dir, "r")
                footer_file = open(footer_file_dir, "r")
                newFilename = get_html_filename(filename)

                top = os.path.dirname(os.path.join(root, filename))
                top2 = top.replace(os.path.join(cwd, "content"), "", 1)
                if platform != "win32":
                    subfolder = top2.replace("/", "", 1)
                else:
                    subfolder = top2.replace("\\", "", 1)

                if subfolder == "":
                    currents_working_file = open(
                        os.path.join(cwd, outdir, newFilename), "w")
                else:
                    create_folder(os.path.join(cwd, outdir, subfolder))
                    currents_working_file = open(os.path.join(
                        cwd, outdir, subfolder, newFilename), "w")

                # Write the header
                currents_working_file.write(header_file.read())

                text_cont1 = convert_text(os.path.join(root, filename))

                if "+++++" in text_cont1.splitlines()[1]:
                    page_template_file = text_cont1.splitlines()[0]
                    text_cont1 = text_cont1.replace(
                        text_cont1.splitlines()[0], "")
                    text_cont1 = text_cont1.replace(
                        text_cont1.splitlines()[1], "")
                else:
                    page_template_file = "content_page"

                # Write the text content into the content template and onto the
                # build file
                content_templ_dir = os.path.join(
                    cwd, "templates", page_template_file + ".html")
                if os.path.exists(content_templ_dir):
                    content_templ_file = open(content_templ_dir, "r")
                    content_templ_file1 = content_templ_file.read()
                    content_templ_file2 = content_templ_file1.replace(
                        "{page_content}", text_cont1)
                    currents_working_file.write(content_templ_file2)
                else:
                    currents_working_file.write(text_cont1)

                # Write the footer to the build file
                currents_working_file.write("\n" + footer_file.read())

                # Close the build file
                currents_working_file.close()

    # Find all the nav(something) templates in the `templates` folder and
    # Read their content to the dict
    navs = {}

    for file in os.listdir(os.path.join(cwd, "templates")):
        if "nav" in file:
            nav_cont = open(os.path.join(cwd, "templates", file), "r")
            navs[file.replace(".html", "")] = nav_cont.read()
            nav_cont.close()

    forbidden_dirs = set(["assets", "templates"])
    blended_version_message = "Built with Blended v" + \
        str(app_version)
    build_date = str(datetime.now().date())
    build_time = str(datetime.now().time())
    build_datetime = str(datetime.now())

    # Replace global variables such as site name and language
    for root, dirs, files in os.walk(os.path.join(cwd, outdir)):
        dirs[:] = [d for d in dirs if d not in forbidden_dirs]
        for filename in files:
            if filename != "config.pyc" and filename != "config.py":
                newFilename = get_html_clear_filename(filename)
                page_file = filename.replace(".html", "")
                page_folder = os.path.basename(os.path.dirname(os.path.join(
                    root, filename))).replace("-", "").replace("_", "").title()
                page_folder_orig = os.path.basename(
                    os.path.dirname(os.path.join(root, filename)))
                top = os.path.dirname(os.path.join(root, filename))
                top2 = top.replace(os.path.join(cwd, outdir), "", 1)
                if platform != "win32":
                    subfolder = top2.replace("/", "", 1)
                else:
                    subfolder = top2.replace("\\", "", 1)
                if subfolder == "":
                    subfolder_folder = os.path.join(cwd, outdir, filename)
                else:
                    subfolder_folder = os.path.join(
                        cwd, outdir, subfolder, filename)
                file_modified = time.ctime(
                    os.path.getmtime(os.path.join(root, filename)))
                file_modified_day = str(datetime.strptime(
                    file_modified, "%a %b %d %H:%M:%S %Y"))[5:7]
                file_modified_year = str(datetime.strptime(
                    file_modified, "%a %b %d %H:%M:%S %Y"))[:4]
                file_modified_month = str(datetime.strptime(
                    file_modified, "%a %b %d %H:%M:%S %Y"))[8:10]

                # The Loop!
                for line in fileinput.input(subfolder_folder, inplace=1):
                    for var in custom_variables:
                        line = line.replace(
                            "{" + var + "}", custom_variables[var])
                    if len(plugins) != 0:
                        for i in range(len(plugins)):
                            if sys.version_info[0] < 2:
                                main = importlib.import_module(plugins[i])
                            elif sys.version_info[0] < 3:
                                main = __import__(plugins[i])
                            content = main.main()
                            line = line.replace(
                                "{" + plugins[i] + "}", content)
                    if "{nav" in line:
                        navname = line.split("{")[1].split("}")[0]
                        line = line.replace(
                            "{" + navname + "}", navs[(line.split("{"))[1].split("}")[0]])
                    line = line.replace(
                        "{website_description}", website_description)
                    line = line.replace(
                        "{website_description_long}", website_description_long)
                    line = line.replace("{website_license}", website_license)
                    line = line.replace("{website_language}", website_language)
                    line = line.replace("{website_url}", website_url)
                    line = line.replace("{author_name}", author_name)
                    line = line.replace("{author_bio}", author_bio)
                    line = line.replace("{random_number}",
                                        str(randint(0, 100000000)))
                    line = line.replace("{build_date}", build_date)
                    line = line.replace("{build_time}", build_time)
                    line = line.replace("{build_datetime}", build_datetime)
                    line = line.replace("{page_list}", page_list)
                    line = line.replace("{page_name}", newFilename)
                    line = line.replace("{page_filename}", page_file)
                    line = line.replace("{page_file}", filename)
                    line = line.replace("{" + filename + "_active}", "active")
                    if page_folder != outdir.title():
                        line = line.replace("{page_folder}", page_folder)
                    else:
                        line = line.replace("{page_folder}", "")
                    if page_folder_orig != outdir:
                        line = line.replace(
                            "{page_folder_orig}", page_folder_orig)
                    else:
                        line = line.replace("{page_folder_orig}", "")
                    line = line.replace("{page_date}", str(file_modified))
                    line = line.replace("{page_day}", str(file_modified_day))
                    line = line.replace("{page_year}", str(file_modified_year))
                    line = line.replace(
                        "{page_month}", str(file_modified_month))
                    line = line.replace("{blended_version}", str(app_version))
                    line = line.replace(
                        "{blended_version_message}", blended_version_message)
                    line = line.replace("{website_name}", website_name)
                    top = os.path.join(cwd, outdir)
                    startinglevel = top.count(os.sep)
                    relative_path = ""
                    level = root.count(os.sep) - startinglevel
                    for i in range(level):
                        relative_path = relative_path + "../"
                    line = line.replace("{relative_root}", relative_path)
                    print(line.rstrip('\n'))
                fileinput.close()

    # Copy the asset folder to the build folder
    if os.path.exists(os.path.join(cwd, "templates", "assets")):
        if os.path.exists(os.path.join(cwd, outdir, "assets")):
            shutil.rmtree(os.path.join(cwd, outdir, "assets"))
        shutil.copytree(os.path.join(cwd, "templates", "assets"),
                        os.path.join(cwd, outdir, "assets"))

    for root, dirs, files in os.walk(os.path.join(cwd, outdir, "assets")):
        for file in files:
            if not file.startswith("_"):
                if (file.endswith(".sass")) or (file.endswith(".scss")):
                    sass_text = open(os.path.join(root, file)).read()
                    text_file = open(os.path.join(
                        root, file[:-4] + "css"), "w")
                    if sass_text != "":
                        text_file.write(sass.compile(string=sass_text))
                    else:
                        print(file + " is empty! Not compiling Sass.")
                    text_file.close()
                if file.endswith(".less"):
                    less_text = open(os.path.join(root, file)).read()
                    text_file = open(os.path.join(
                        root, file[:-4] + "css"), "w")
                    if less_text != "":
                        text_file.write(lesscpy.compile(StringIO(less_text)))
                    else:
                        print(file + " is empty! Not compiling Less.")
                    text_file.close()
                if file.endswith(".styl"):
                    try:
                        styl_text = open(os.path.join(root, file)).read()
                        text_file = open(os.path.join(
                            root, file[:-4] + "css"), "w")
                        if styl_text != "":
                            text_file.write(Stylus().compile(styl_text))
                        else:
                            print(file + " is empty! Not compiling Styl.")
                        text_file.close()
                    except:
                        print("Not able to build with Stylus! Is it installed?")
                        try:
                            subprocess.call["npm", "install", "-g", "stylus"]
                        except:
                            print("NPM (NodeJS) not working. Is it installed?")
                if file.endswith(".coffee"):
                    coffee_text = open(os.path.join(root, file)).read()
                    text_file = open(os.path.join(root, file[:-6] + "js"), "w")
                    if coffee_text != "":
                        text_file.write(coffeescript.compile(coffee_text))
                    else:
                        print(file + " is empty! Not compiling CoffeeScript.")
                    text_file.close()
                if minify_css:
                    if file.endswith(".css"):
                        css_text = open(os.path.join(root, file)).read()
                        text_file = open(os.path.join(root, file), "w")
                        if css_text != "":
                            text_file.write(cssmin(css_text))
                        text_file.close()
                if minify_js:
                    if file.endswith(".js"):
                        js_text = open(os.path.join(root, file)).read()
                        text_file = open(os.path.join(root, file), "w")
                        if js_text != "":
                            text_file.write(jsmin(js_text))
                        text_file.close()


@cli.command('build', short_help='Build the Blended files into a website')
@click.option('--outdir', default="build", help='Choose which folder to build to. Default is `build`.')
def build(outdir):
    """Blends the generated files and outputs a HTML website"""

    print("Building your Blended files into a website!")

    reload(sys)
    sys.setdefaultencoding('utf8')

    build_files(outdir)

    print("The files are built! You can find them in the " + outdir +
          "/ directory. Run the view command to see what you have created in a web browser.")


outdir_type = "build"


class Watcher:
    DIRECTORY_TO_WATCH = os.path.join(cwd, "content")

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        threads = []
        paths = [os.path.join(cwd, "content"), os.path.join(cwd, "templates")]

        for i in paths:
            targetPath = str(i)
            self.observer.schedule(event_handler, targetPath, recursive=True)
            threads.append(self.observer)

        self.observer.start()

        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("\nObserver stopped.")

        self.observer.join()


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        global outdir_type
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            # Take any action here when a file is first created.
            build_files(outdir_type)
            print("%s created" % event.src_path)

        elif event.event_type == 'modified':
            # Taken any action here when a file is modified.
            build_files(outdir_type)
            print("%s modified" % event.src_path)

        elif event.event_type == 'deleted':
            # Taken any action here when a file is modified.
            build_files(outdir_type)
            print("%s deleted" % event.src_path)


@cli.command('interactive', short_help='Build the Blended files into a website on each file change')
@click.option('--outdir', default="build", help='Choose which folder to build to. Default is `build`.')
def interactive(outdir):
    """Blends the generated files and outputs a HTML website on file change"""

    print("Building your Blended files into a website!")

    global outdir_type
    outdir_type = outdir

    reload(sys)
    sys.setdefaultencoding('utf8')

    build_files(outdir)

    print("Watching the content and templates directories for changes, press CTRL+C to stop...\n")

    w = Watcher()
    w.run()


@cli.command('view', short_help='View the finished Blended website')
@click.option('--outdir', default="build", help='Choose which folder the built files are in. Default is `build`.')
def view(outdir):
    """Opens the built index.html file in a web browser"""

    index_path = os.path.realpath(os.path.join(cwd, outdir, "index.html"))
    if os.path.exists(index_path):
        webbrowser.open('file://' + index_path)
    else:
        print("The index.html file could not be found in the " + outdir +
              "/ folder! Have you deleted it or have you built with home_page_list set to 'no' in config.py?")


if __name__ == '__main__':
    cli()
