from flask import Flask
web_app = Flask(__name__)

# Very important, get the directory that the user wants to run commands in
cwd = os.getcwd()

@web_app.route("/")
def hello():
    return "Hello World!"
