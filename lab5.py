from flask import  render_template, Blueprint, request, redirect, session
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
lab5 = Blueprint('lab5', __name__)


@lab5.route('/lab5/')
def lab():
    name = request.cookies.get('name')

    if name is None:
        name = "Anonymous"
    return render_template('lab5/lab5.html', name=name)


def db_connect():
    conn = psycopg2.connect(
        host = '127.0.0.1',
        database = 'anastasia_kuzmina_knowledge_base',
        user = 'anastasia_kuzmina_knowledge_base',
        password = '123'
    )
    cur = conn.cursor(cursor_factory = RealDictCursor)

    return conn, cur


def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()


@lab5.route('/lab5/register/', methods = ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')
    
    login = request.form.get('login')
    password = request.form.get('password')

    if not (login or password):
        return render_template('lab5/register.html', error='Заполните все поля!')
    
    conn, cur = db_connect()

    cur.execute("SELECT login FROM users WHERE login=%s;", (login, ))
    if cur.fetchone():
        db_close(conn, cur)
        return render_template ('lab5/register.html', error='Такой пользователь уже существует')
    
    password_hash = generate_password_hash(password)
    cur.execute("INSERT INTO users (login, password) VALUES (%s, %s)", (login, password_hash))

    db_close(conn, cur)
    return render_template('lab5/success.html', login=login)


