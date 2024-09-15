from flask import Flask, url_for, redirect
app = Flask(__name__)

@app.route("/web")
def web():
    return """<!DOCTYPE html>
            <html>
                <body>
                    <h1>web-сервер на flask</h1>
                    <a href="/author">http://127.0.0.1:5000/author</a>
                </body>
            </html>""", 200, {"X-Server": "sample",
                              "Content-Type": "text/plain; charset=utf-8"}

@app.route("/author")
def author():
    name = "Кузьмина Анастасия Станиславовна"
    group = "ФБИ-22"
    faculty = "ФБ"

    return """<!DOCTYPE html>
            <html>
                <body>
                    <p>Студент: """ + name + """</p>
                    <p>Группа: """ + group + """</p>
                    <p>Факультет: """ + faculty + """</p>
                    <a href="/web">http://127.0.0.1:5000/web</a>
                </body>
            </html>"""

@app.route("/lab1/oak")
def oak():
    path = url_for("static", filename="oak.jpg")
    style = url_for("static", filename="lab1.css")
    return '''
<!DOCTYPE html>
<html>
    <head>
    <link rel="stylesheet" type="text/css" href="''' + style + '''">
    </head>
    <body>
        <h1>Дуб</h1>
        <img src="'''+path+'''">
    </body>
</html>
'''
count=0
@app.route("/lab1/counter")
def counter():
    global count
    count+=1
    return'''
<!DOCTYPE html>
<html>
    <body>
        Сколько раз вы сюда заходили: '''+ str(count) +'''
        <br>
        <a href="/lab1/counter/reset">Сбросить счётчик</a>
    </body>
</html>
'''

@app.route("/info")
def info():
    return redirect("/author")

@app.route("/lab1/created")
def created():
    return'''
<!DOCTYPE html>
<html>
    <body>
        <h1>Создано успешно</h1>
        <div><i>что-то создано...</i></div>
    </body>
</html>
''', 201

@app.errorhandler(404)
def not_found(err):
    return "ТАКОЙ СТРАНИЦЫ НЕ СУЩЕСТВУЕТ", 404


@app.route('/lab1/counter/reset')
def reset_counter():
    global count
    count = 0
    return'''
<!DOCTYPE html>
<html>
    <body>
        Сколько раз вы сюда заходили: '''+ str(count) +'''
        <br>
        <a href="/lab1/counter">Возобновить счетчик</a>
    </body>
</html>'''