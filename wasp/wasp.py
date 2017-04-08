# -*- coding: utf-8 -*-
"""
    Wasp
    ~~~~~~

    A flask application madewith sqlite3, oauth2, sqlalchemy

    Author: Julu Ahamed
"""
import os
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

from .database import db_session

UPLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), 'media/images'))

# create our little application :)
app = Flask(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='development key',
    UPLOAD_FOLDER=UPLOAD_FOLDER
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

from views import showRoot, newCategory, showLogin, gconnect, gdisconnect, newItem, showCategory, uploadedFile
from views import viewCategory, viewItem, addImage, errorNotFound, deleteItemImage, editItem

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


