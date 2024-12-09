from dotenv import load_dotenv
load_dotenv()
import os
from flask import Blueprint, render_template, jsonify
from database.DatabaseFactory import DatabaseFactory

from database.sqlite.models import File, Hashtag, Page

bp = Blueprint('routes', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/data/files')
def files():
    database = DatabaseFactory.create_database(os.getenv('DB_TYPE'))
    database.connect()

    files = database.sessionLocal().query(File).all()
    files = [file.to_dict() for file in files]
    return jsonify(files)

@bp.route('/data/pages')
def pages():
    database = DatabaseFactory.create_database(os.getenv('DB_TYPE'))
    database.connect()

    pages = database.sessionLocal().query(Page).all()
    pages = [page.to_dict() for page in pages]
    
    return jsonify(pages)

@bp.route('/data/hashtags')
def hashtags():
    database = DatabaseFactory.create_database(os.getenv('DB_TYPE'))
    database.connect()

    hashtags = database.sessionLocal().query(Hashtag).all()
    hashtags = [hashtag.to_dict() for hashtag in hashtags]
    
    return jsonify(hashtags)
    