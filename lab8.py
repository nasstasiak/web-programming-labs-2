import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
from os import path
from flask import  render_template, Blueprint, request, jsonify, current_app
from datetime import datetime

lab8 = Blueprint('lab8', __name__)


def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host = '127.0.0.1',
            database = 'anastasia_kuzmina_knowledge_base',
            user = 'anastasia_kuzmina_knowledge_base',
            password = '123'
        )
        cur = conn.cursor(cursor_factory = RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()


@lab8.route('/lab8/')
def main():
    return render_template('lab7/lab7.html')


