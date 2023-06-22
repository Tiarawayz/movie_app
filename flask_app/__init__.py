from flask import Flask
app = Flask (__name__)
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = 'dontactout'