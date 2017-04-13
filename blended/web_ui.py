import os
from flask import Flask, render_template
web_app = Flask(__name__, template_folder="web_templates")

# Very important, get the directory that the user wants to run commands in
cwd = os.getcwd()

@web_app.route("/")
def hello():
    return "Hello World! The cwd is: %s" % cwd

@web_app.route("/edit/<filename>")
def edit_file(filename):
    content = open(os.path.join(cwd, "content", filename), 'r').read()
    return render_template('edit.html', content=content)
