import os
from flask import Flask, render_template, request, url_for, redirect
web_app = Flask(__name__, template_folder="web_templates")

# Very important, get the directory that the user wants to run commands in
cwd = os.getcwd()

@web_app.route("/")
def hello():
    return "Hello World! The cwd is: %s" % cwd

@web_app.route("/edit/<filename>")
def edit_file(filename):
    content = open(os.path.join(cwd, "content", filename), 'r').read()
    return render_template('edit.html', content=content, filename=filename)

@web_app.route("/publish/", methods=['POST'])
def publish():
    content = request.form['code']
    filename = request.form['filename']

    with open(os.path.join(cwd, "content", filename), 'w') as wfile:
        wfile.write(content)

    return redirect("/edit/"+filename+"?finished=yes", code=302)
