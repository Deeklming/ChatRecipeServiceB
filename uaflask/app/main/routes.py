from app.main import bp
from flask import render_template, redirect, url_for
from flask_login import current_user
from flask import jsonify

@bp.route('/', methods=['GET'])
def index():
    return jsonify({"test": "ok"})
