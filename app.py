from flask import Flask
import os

app = Flask(__name__)
app.secret_key = "secret key"

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app.config["TEST_PATH"] = os.path.join(APP_ROOT, 'static/')