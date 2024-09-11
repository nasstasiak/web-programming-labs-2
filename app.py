from flask import Flask, url_for
app = Flask(__name__)

@app.route("/web")
def web():
    return """<!DOCTYPE html>
            <html>
                <body>
                    <h1>web-сервер на flask</h1>
                    <a href="/author">http://127.0.0.1:5000/author</a>
                </body>
            </html>"""

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
    return '''
<!DOCTYPE html>
<html>
    <body>
        <h1>Дуб</h1>
        <img src="'''+path+'''">
    </body>
</html>
'''