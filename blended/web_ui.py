import os
from flask import Flask, render_template, request, url_for, redirect
web_app = Flask(__name__, template_folder="web_templates")

# Very important, get the directory that the user wants to run commands in
cwd = os.getcwd()


@web_app.route("/")
def dashboard():
    published_files = 0
    unpublished_files = 0
    for root, dirs, files in os.walk(os.path.join(cwd, "content")):
        dirs[:] = [d for d in dirs if "_" not in d]
        for filename in files:
            if not filename.startswith("_"):
                published_files = published_files + 1
            else:
                unpublished_files = unpublished_files + 1

    return render_template('dashboard.html', published=published_files, unpublished=unpublished_files)


@web_app.route("/files/")
def files():
    file_list = ""
    for root, dirs, files in os.walk(os.path.join(cwd, "content")):
        dirs[:] = [d for d in dirs if "_" not in d]
        for filename in files:
            dirname = root.split(os.path.sep)[-1]
            if dirname == "content":
                output = filename
            else:
                output = os.path.join(dirname, filename)

            file_list = file_list + "<a href=\"/edit/"+output.replace("\\", "/")+"\" class=\"list-group-item list-group-item-action\">"+filename+"</a>\n"

    return render_template('files.html', file_list=file_list)


@web_app.route("/edit/<path:filename>")
def edit_file(filename):
    content = open(os.path.join(cwd, "content", filename), 'r').read()
    return render_template('edit.html', content=content, filename=filename)


@web_app.route("/edit/")
def edit_redirect():
    return redirect("/files/", code=302)


@web_app.route("/publish/", methods=['POST'])
def publish():
    content = request.form['code']
    filename = request.form['filename']

    with open(os.path.join(cwd, "content", filename), 'w') as wfile:
        wfile.write(content)

    return redirect("/edit/" + filename + "?finished=yes", code=302)
