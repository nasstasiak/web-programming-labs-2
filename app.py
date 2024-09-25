from flask import Flask, url_for, redirect, render_template
app = Flask(__name__)

@app.route("/lab1/web")
def web():
    return """<!DOCTYPE html>
            <html>
                <body>
                    <h1>web-сервер на flask</h1>
                    <a href="/author">http://127.0.0.1:5000/author</a>
                </body>
            </html>""", 200, {"X-Server": "sample",
                              "Content-Type": "text/plain; charset=utf-8"}

@app.route("/lab1/author")
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

@app.route("/lab1/info")
def info():
    return redirect("/lab1/author")

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
        <a href="/lab1">Лабораторная работа 1</a>
        </div>
    </main>

    <footer>
        &COPY; Кузьмина Анастасия, ФБИ-22, 3 курс, 2024
    </footer>
</body>
</html>
'''

@app.route('/lab1')
def lab1():
    style = url_for("static", filename="style.css")
    return '''<!DOCTYPE html>
<head>
    <title>Лабораторная работа 1</title>
    <link rel="stylesheet" type="text/css" href="''' + style + '''">
    <link rel="shortcut icon" href="dog.png" type="image/x-icon">
</head>
<body >
    <header>
        Лабораторная работа 1
    </header>
    <main>
        <div>
            Flask — фреймворк для создания веб-приложений на языке программирования Python, использующий набор инструментов
            Werkzeug, а также шаблонизатор Jinja2. Относится к категории так называемых микрофреймворков — минималистичных каркасов
            веб-приложений, сознательно предоставляющих лишь самые базовые возможности.<br>
            <a href="/">Меню лабораторных работ</a>
        </div>
         <h2 style="text-align: center; font-family: cursive; color: rgb(85, 107, 47);">Список роутов</h2>
        <div style="margin-left: 45%;">
            <a href="/lab1/web">web</a><br>
            <a href="/lab1/author">author</a><br>
            <a href="/lab1/oak">oak</a><br>
            <a href="/lab1/counter">counter</a><br>
            <a href="/lab1/counter/reset">reset</a><br>
            <a href="/lab1/info">info</a><br>
            <a href="/lab1/created">created</a><br>
            <a href="/lab1/errors">errors</a><br>
            <a href="/lab1/headers">headers</a><br>
            <a href="/lab1/tower">tower</a><br>
        </div>
    </main>

    <footer>
        &COPY; Кузьмина Анастасия, ФБИ-22, 3 курс, 2024
    </footer>
</body>
</html>
'''

@app.route("/lab1/errors")
def errors():
   style = url_for("static", filename="style.css")
   return '''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="''' + style + '''">
    </head>
    <body style="padding: 10px;">
        <a href="/lab1/bad_request">400;</a><br>
        <a href="/lab1/unauthorized">401;</a><br>
        <a href="/lab1/payment_required">402;</a><br>
        <a href="/lab1/forbidden">403;</a><br>
        <a href="/lab1/not_found">404;</a><br>
        <a href="/lab1/method_not_allowed">405;</a><br>
        <a href="/lab1/teapot">418;</a><br>
        <a href="/lab1/internal_server_error">500;</a><br>
        <a href="/lab1">&#128072;</a>
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

@app.route("/lab1/bad_request")
def bad_request():
    return "Ошибка 400. Неправильный синтаксис", 400

@app.route("/lab1/unauthorized")
def unauthorized():
    return "Ошибка 401. Неавторизованный доступ", 401

@app.route("/lab1/payment_required")
def payment_required():
    return "Ошибка 402. Требуется оплата", 402

@app.route("/lab1/forbidden")
def forbidden():
    return "Ошибка 403. Доступ запрещён", 403

@app.route("/lab1/method_not_allowed")
def method_not_allowed():
    return "Ошибка 405. Метод не поддерживается целевым ресурсом", 405

@app.route("/lab1/teapot")
def teapot():
    return "Ошибка 418. Сервер не может приготовить кофе, потому что он чайник", 418

@app.route('/lab1/internal_server_error')
def internal_server_error():
    result = 100 / 0  
    return 'Результат: ' + str(result)

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

@app.route("/lab1/headers")
def headers():
    island = url_for("static", filename="island.webp")
    return '''
<!doctype html>
<html>
<head>
    <style>
        img {
            top: 0;
            width: 100%;
            z-index: -1;
            position: absolute;
            margin-top: 0;
        }
        body {
            margin: 0;
            padding: 0;
            font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
        }
        h1, h2, div {
            margin: 10px;
            text-align: justify;
            color: #042c5e;
        }
        h1 {
            text-align: center;
            font-family: cursive;
            margin-bottom: 0;
        }
        div {
            line-height: 1.25;
            text-indent: 1.2cm;
            margin-top: 2px;
            padding-left: 10px;
            padding-right: 5px;
            font-size: 11pt;
        }
        p {
            text-indent: 1.2cm;
            margin-top: 0;
            margin-bottom: 2px;
        }
    </style>
</head>
    <body>  
        <img src="'''+ island +'''">      
        <h1>Летний сон в алых тонах</h1>
        <div>
            Чудесным теплым днем я поднимаюсь на борт судна и отправляюсь навстречу новой жизни.<br>
            <p>Судно, которое увезет меня прочь от всего, что было. К чему-то совершенно новому.</p>
<p>Прочь от всего, что вместили последние месяцы.</p>
        </div>
        <div>
            От всех слез, от всех бессонных ночей, проведенных перед телевизором в компании мороженого. 
            Или как оно там должно выглядеть. Во всяком случае, я всегда именно так представляла себе расставание. 
            Ну ладно, возможно, кто-нибудь на моем месте махнул бы в Австралию, прыгнул с тарзанки или пустился бы вплавь 
            по Нилу на крокодиле, чтобы вновь обрести себя. Но что может быть лучше проверенного киношного способа справиться 
            с навалившимся отчаянием – выплакать все слезы, которые необходимо выплакать, и съесть все мороженое, которое 
            необходимо съесть. Очень-очень много мороженого.
        </div>
        <div>
            И я попробовала. Накупила кучу коробок с мороженым, сколько смогла унести. Но мой желудок запротестовал уже 
            после двух. Лактоза уничтожила мои шансы на киношную скорбь. Оставалось просто лежать на диване. 
            В полном одиночестве. И глазеть на мир через экран телевизора. На мир, который внезапно стал чужим и далеким.
        </div>
        <div>
            Мой чемодан на колесиках скрипит по гравию. Я прохожу мимо киоска с мороженым и еще парочки лавок, торгующих 
            жареной салакой и свежими креветками. За спиной – гостевая бухта, где приезжающие швартуют свои парусные яхты 
            в преддверии праздника. Я прочитала, что где-то здесь есть гостиница. И даже небольшой магазин «ИКА» и ресторанчик, 
            в котором подают пиццу и гамбургеры с маринованным луком (я много раз гуглила меню в Интернете, и надо сказать, 
            я просто обожаю маринованный лук). Но впереди справа я уже вижу вывеску, обозначающую вход в Буллхольменский 
            садоводческий кооператив. Я останавливаюсь и наклоняюсь к моему маленькому розовому чемоданчику на колесиках. 
            Достаю из кармана смартфон и делаю снимок, который тут же отправляю Закке с текстом: Я на месте!
        </div>
    </body>
</html>''', 200, {
    'X-first': 'one',
    'X-second': 'two',
    'Content-Language': 'ru-RU'
    }


tower_built = False

@app.route('/lab1/tower')
def teacup_status():
    style = url_for("static", filename="style.css")
    global tower_built
    status = "Башня построена" if tower_built else "Башня не построена"
    return '''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="''' + style + '''">
    </head>
    <body>
        <h1>'''+status+'''</h1>
        <a href="/lab1/built">Построить башню</a><br>
        <a href="/lab1/drop">Снести башню</a>
    </body>
</html>
''', 200

@app.route('/lab1/built')
def create_tower():
    style = url_for("static", filename="style.css")
    tower = url_for("static", filename="tower.png")
    global tower_built
    
    if tower_built:
        return '''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="''' + style + '''">
    </head>
    <body>
        <p>Башня уже построена</p>
        <img src="'''+ tower +'''" style="margin-left:30%;">  <br>
        <a href="/lab1/tower">&#128072;</a><br>
    </body>
</html>
''', 400
    else:
        tower_built = True
        return '''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="''' + style + '''">
    </head>
    <body>
        <p>Башня успешно построена)</p>
        <img src="'''+ tower +'''" style="margin-left:30%;"> <br>
        <a href="/lab1/tower">&#128072;</a><br>
    </body>
</html>
''', 201

@app.route('/lab1/drop')
def drop_tower():
    style = url_for("static", filename="style.css")
    ruin = url_for("static", filename="ruins.png")
    global tower_built    
    if tower_built:
        tower_built = False
        return '''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="''' + style + '''">
    </head>
    <body>
        <p>Башня снесена</p>
        <img src="'''+ ruin +'''" style="margin-left:30%;">  <br>
        <a href="/lab1/tower">&#128072;</a><br>
    </body>
</html>
''', 200
    
    else:
        return '''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="''' + style + '''">
    </head>
    <body>
        <p>Теперь нужно строить новую башню((</p>
        <img src="'''+ ruin +'''" style="margin-left:30%;">  <br>
        <a href="/lab1/tower">&#128072;</a><br>
    </body>
</html>
''', 400
    

@app.route('/lab2/a/')
def a():
    return "ok"

@app.route('/lab2/a')
def a2():
    return "not ok"

flower_list = ['роза', 'тюльпан', 'незабудка', 'ромашка']

@app.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flower_list):
        return "Такого цветка нет", 404
    else:
        return "цветок: " + flower_list[flower_id]


 
@app.route('/lab2/add_flower/<name>')
def add_flower(name):
    flower_list.append(name)
    return f"""<!DOCTYPE html>
            <html>
                <body>
                    <h1>Добавлен новый цветок</h1>
                    <p>Название нового цветка: {name} </p>
                    <p>Всего цветов: {len(flower_list)} </p>
                    <p>Полный список: {flower_list} </p>
                </body>
            </html>"""



@app.route('/lab2/example')
def example():
    lab_num, name, group, course= '2', 'Кузьмина Анастасия','ФБИ-22', '3'
    return render_template('example.html', name=name, lab_num=lab_num, group=group, course=course)