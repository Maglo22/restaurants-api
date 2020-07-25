import functools
from os import name
from sqlite3.dbapi2 import Statement

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from werkzeug.exceptions import abort
from api.db import get_db

bp = Blueprint('site', __name__)

# site index
@bp.route('/', methods=['GET'])
def index():
    return render_template('site/index.html')