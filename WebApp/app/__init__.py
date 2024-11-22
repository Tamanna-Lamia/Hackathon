from flask import Flask
from config import Config
from flask import redirect, url_for
from flask import send_file
import os

app = Flask(__name__)
app.config.from_object(Config)

from app import routes
