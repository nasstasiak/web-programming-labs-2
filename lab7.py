from flask import Blueprint, render_template, request, redirect, session, current_app
from os import path
import sqlite3
import psycopg2
from psycopg2.extras import RealDictCursor

lab7 = Blueprint('lab7', __name__)


@lab7.route('/lab7/')
def main():
    return render_template('lab7/index.html')
