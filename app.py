import os
from os import path
from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from db import db

from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
from lab6 import lab6
from lab7 import lab7
from lab8 import lab8


app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SEKRET_KEY', 'секретно-секретный-секрет')
app.config['DB_TYPE'] = os.environ.get('DB_TYPE', 'postgres')

if app.config['DB_TYPE'] == 'postgres':
    db_name = 'anastasiia_kuzmina_orm'
    db_user = 'anastasiia_kuzmina_orm'
    db_password = '123'
    host_ip = '127.0.0.1'
    host_port = 5432

    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{host_ip}:{host_port}/{db_name}'
else:
    dir_path = path.dirname(path.realpath(__file__))
    db_path = path.join(dir_path, "anastasiia_kuzmina_orm.db")
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

db.init_app(app)   



app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)
app.register_blueprint(lab6)
app.register_blueprint(lab7)
app.register_blueprint(lab8)


@app.errorhandler(404)
def not_found(err):
    return "ТАКОЙ СТРАНИЦЫ НЕ СУЩЕСТВУЕТ", 404


@app.route("/")
@app.route("/index")
def labs():
    style = url_for("static", filename="style.css")
    return '''<!DOCTYPE html>
<head>
    <title>НГТУ, ФБ, Лабораторные работы</title>
    <link rel="stylesheet" type="text/css" href="''' + style + '''">
    <link rel="shortcut icon" href="dog.png" type="image/x-icon">
</head>
<body >
    <header>
        НГТУ, ФБ, WEB-программирование,часть 2. Список лабораторных
    </header>
    <main>
        <h1>Лабораторные работы по WEB-программированию</h1>
        <div>
        <a href="/lab1">Лабораторная работа 1</a><br>
        <a href="/lab2/">Лабораторная работа 2</a><br>
        <a href="/lab3">Лабораторная работа 3</a><br>
        <a href="/lab4">Лабораторная работа 4</a><br>
        <a href="/lab5">Лабораторная работа 5</a><br>
        <a href="/lab6/">Лабораторная работа 6</a><br>
        <a href="/lab7/">Лабораторная работа 7</a>
        </div>
    </main>

    <footer>
        &COPY; Кузьмина Анастасия, ФБИ-22, 3 курс, 2024
    </footer>
</body>
</html>
'''


@app.errorhandler(404)
def not_found(err):
    error = url_for("static", filename="error.png")
    return '''
<!doctype html>
<html>
    <head>
        <style>
            img {
                width: 55%;
            }
            body {
                color: red;
                font-weight: bold;
                font-size: 24pt;
                font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
                text-align: center;
                background-color: rgb(242, 242, 242);
            }
        </style>
    </head>
    <body>
        <img src="'''+ error +'''"><br>
        <p style="font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif; color: red; font-size: 24pt;">
            Упс! Кажется, что-то пошло не так...
        </p>
    </body>
</html>
''', 404


@app.errorhandler(500)
def internal_server(error):
    return '''
<!doctype html>
<html>
    <head>
        <style>
            body {
                margin-top: 18%;
                font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
                text-align: center;
                background-color: rgb(242, 242, 242);
            }
            h1 {
                color: red;
                font-weight: bold;
                font-size: 24pt;         
            }
            p {
                color: grey;
                font-size: 14pt;
            }
            div {
                background-color: white;
                box-shadow: 0 0 15px grey;
                border-radius: 15px;
                padding: 5px;
            }
        </style>
    </head>
    <body>
        <div>
            <h1>На сервере произошла ошибка</h1>
            <p>Попробуйте зайти на страницу позже<br></p>
        </div>
    </body>
</html>
''', 500  

