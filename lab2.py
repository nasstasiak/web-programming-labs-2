from flask import Blueprint, url_for, redirect, render_template, request
lab2 = Blueprint('lab2', __name__)

@lab2.route('/lab2/a/')
def a():
    return "ok"

@lab2.route('/lab2/a')
def a2():
    return "not ok"

#flower_list = ['роза', 'тюльпан', 'незабудка', 'ромашка']

@lab2.route('/lab2/example')
def example():
    lab_num, name, group, course= '2', 'Кузьмина Анастасия','ФБИ-22', '3'
    fruits = [
        {'name': 'яблоки', 'price': 100}, 
        {'name': 'груши', 'price': 120},
        {'name': 'мандарины', 'price': 96},
        {'name': 'манго', 'price': 315},
        {'name': 'персики', 'price': 140},
        ]
    return render_template('example.html', name=name, lab_num=lab_num, group=group, course=course, fruits=fruits)


@lab2.route('/lab2/')
def lab():
    return render_template('lab2.html')


@lab2.route('/lab2/filters/')
def filters():
    phrase = 'О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных...'
    return render_template('filter.html', phrase=phrase)

flower_list = [
    {'name': 'Роза', 'price': 70},
    {'name': 'Лилия', 'price': 120},
    {'name': 'Гиацинт', 'price': 90},
    {'name': 'Тюльпан', 'price': 60},
    {'name': 'Орхидея', 'price': 180}
]


@lab2.route('/lab2/flowers/<int:flower_id>/')
def flowers(flower_id):
    style = url_for("static", filename="style.css")
    if flower_id >= len(flower_list):
        return '''<!doctype html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="''' + style + '''">
    </head>
    <body>
        <h1>Такого цветка еще нет&#128577;</h1>
    </body>
</html>
''', 404
    else:
        flower = flower_list[flower_id]
    return render_template('flower_detail.html', flower=flower, flower_id=flower_id)   


@lab2.route('/lab2/flowers/')
def all_flowers():
    flowers=flower_list
    length = len(flower_list)
    return render_template('flowers.html', flower_list=flowers, length=length)


@lab2.route('/lab2/add_flower/')
def add_flower():
    name = request.args.get('name')
    price = request.args.get('price')
    style = url_for("static", filename="style.css")
    if name and price:
        flower_list.lab2end({'name': name, 'price': int(price)})
        flower_id = len(flower_list) - 1
        return redirect(url_for('flowers', flower_id=flower_id))    
    return '''<!doctype html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="''' + style + '''">
    </head>
    <body>
        <h1>Вы не задали имя и цену цветка&#128577;</h1>
    </body>
</html>
''', 400


'''
@lab2.route('/lab2/all_flowers/')
def all_flowers():
    flowers=flower_list
    length = len(flower_list)
    return render_template('flowers.html', flower_list=flowers, length=length)
'''


@lab2.route('/lab2/del_flowers/')
def del_flowers():
    #style = url_for("static", filename="style.css")
    flower_list.clear()  
    return  redirect(url_for('all_flowers'))

#<!doctype html>
#<html>
#    <head>
 #       <link rel="stylesheet" type="text/css" href="''' + style + '''">
  #  </head>
   # <body>
    #    <h1>Список цветов успешно очищен!</h1>
     #   <p><a href="/lab2/all_flowers/">Вернуться к списку цветов</a></p>
   #</html>'''

@lab2.route('/lab2/delete_flower/<int:flower_id>/')
def delete_flower(flower_id):
    style = url_for("static", filename="style.css")
    if flower_id >= len(flower_list):
        return '''<!doctype html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="''' + style + '''">
    </head>
    <body>
        <h1>Нет цветка с таким номером&#128577;</h1>
    </body>
</html>
''', 404  
    else:
        del flower_list[flower_id] 
        return redirect(url_for('all_flowers'))


@lab2.route('/lab2/calc/<int:a>/<int:b>')
def calculate(a, b):
    addition = a + b
    subtraction = a - b
    multiplication = a * b
    division = a / b if b != 0 else ":(("
    power = a ** b

    return render_template('calc.html',
                           a=a,
                           b=b,
                           addition=addition,
                           subtraction=subtraction,
                           multiplication=multiplication,
                           division=division,
                           power=power)


@lab2.route('/lab2/calc/')
def default_calc():
    return redirect(url_for('calculate', a=1, b=1))


@lab2.route('/lab2/calc/<int:a>')
def single_number_calc(a):
    return redirect(url_for('calculate', a=a, b=1))


books = [
    {"author": "Джон Стейнбек", "title": "О мышах и людях", "genre": "Классика", "pages": 107},
    {"author": "Джейн Остин", "title": "Гордость и предубеждение", "genre": "Роман", "pages": 432},
    {"author": "Чарльз Диккенс", "title": "Великие надежды", "genre": "Классика", "pages": 597},
    {"author": "Агата Кристи", "title": "Десять негритят", "genre": "Детектив", "pages": 256},
    {"author": "Стивен Кинг", "title": "Сияние", "genre": "Ужасы", "pages": 451},
    {"author": "Джордж Оруэлл", "title": "1984", "genre": "Антиутопия", "pages": 328},
    {"author": "Фрэнк Херберт", "title": "Дюна", "genre": "Научная фантастика", "pages": 412},
    {"author": "Рэй Брэдбери", "title": "451 градус по Фаренгейту", "genre": "Научная фантастика", "pages": 174},
    {"author": "Джоан Роулинг", "title": "Гарри Поттер и философский камень", "genre": "Фэнтези", "pages": 223},
    {"author": "Дэн Браун", "title": "Код да Винчи", "genre": "Триллер", "pages": 454},
]

@lab2.route("/lab2/books")
def book():
    return render_template("books.html", books=books)


birds = [
    {
        "name": "Воробьи",
        "image": "bird1.png",
        "description": "Воробьи — одни из самых распространенных птиц в мире, обитающие в различных климатических зонах."
    },
    {
        "name": "Совы",
        "image": "bird2.png",
        "description": "Совы — хищные птицы, известные своим ночным образом жизни, отличным зрением и слухом."
    },
    {
        "name": "Голуби",
        "image": "bird3.png",
        "description": "Голуби — птицы, широко распространенные в городских и сельских районах, известны своей способностью к полету на дальние расстояния."
    },
    {
        "name": "Дятлы",
        "image": "bird4.png",
        "description": "Дятлы — птицы, которые известны своей способностью долбить древесину, чтобы найти насекомых и создать дупло для гнездования."
    },
    {
        "name": "Колибри",
        "image": "bird5.png",
        "description": "Колибри — самые маленькие птицы в мире, известные своим быстрым полетом и способностью парить в воздухе."
    }
]

@lab2.route('/lab2/birds/')
def birds_page():
    return render_template('birds.html', birds=birds)  

