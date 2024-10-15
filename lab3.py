from flask import Blueprint, render_template, request, make_response, redirect, url_for
lab3 = Blueprint('lab3', __name__)


@lab3.route('/lab3/')
def lab():
    name = request.cookies.get('name')
    name_color = request.cookies.get('name_color')
    age = request.cookies.get('age')
    if name is None:
        name = "Anonimous"
    if age is None:
        age = "unknown"
    return render_template('lab3/lab3.html', name= name, name_color = name_color, age=age)


@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name', 'Alex', max_age=5)
    resp.set_cookie('age', '20')
    resp.set_cookie('name_color', 'magenta')
    return resp


@lab3.route('/lab3/del_cookie/')
def del_cookie():
    resp = make_response(redirect('/lab3/'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.delete_cookie('name_color')
    return resp


@lab3.route('/lab3/form1/')
def form1():
    errors = {}
   
    user = request.args.get('user')
    
    if user == '':
        errors ['user'] = 'Заполните поле "Имя"'

    age = request.args.get('age')
    if age == '':
        errors['age'] = 'Заполните поле "Возраст"'

    sex = request.args.get('sex')
    return render_template('/lab3/form1.html', user=user, age=age, sex=sex, errors=errors)


@lab3.route('/lab3/order/')
def order():
    return render_template('lab3/order.html')


price = 0

@lab3.route('/lab3/pay/')
def pay():
    global price

    drink = request.args.get('drink')
    if drink == 'coffee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else:
        price = 70

    if request.args.get('milk') == 'on':
        price += 30
    if request.args.get('sugar') == 'on':
        price += 10
        
    return render_template('lab3/pay.html', price=price)


@lab3.route('/lab3/paid/')
def paid():
    global price 
    
    return render_template('lab3/paid.html', price=price)


@lab3.route('/lab3/settings/')
def settings():
    color = request.args.get('color')
    bgcolor = request.args.get('bgcolor')
    fsize = request.args.get('fsize')
    fontfamily = request.args.get('fontfamily')
    textalign = request.args.get('textalign')

    if color:
        resp = make_response(redirect('/lab3/settings/'))
        resp.set_cookie('color', color)
        return resp
    if bgcolor:
        resp = make_response(redirect('/lab3/settings/'))
        resp.set_cookie('bgcolor', bgcolor)
        return resp
    if fsize:
        resp = make_response(redirect('/lab3/settings/'))
        resp.set_cookie('fsize', fsize)
        return resp
    if fontfamily:
        resp = make_response(redirect('/lab3/settings/'))
        resp.set_cookie('fontfamily', fontfamily)
        return resp
    if textalign:
        resp = make_response(redirect('/lab3/settings/'))
        resp.set_cookie('textalign', textalign)
        return resp
    
    color = request.cookies.get('color')
    bgcolor = request.cookies.get('bgcolor') 
    fsize = request.cookies.get('fsize') 
    fontfamily  = request.cookies.get('fontfamily')
    resp = make_response(render_template('lab3/settings.html', color=color, bgcolor=bgcolor,fsize=fsize, fontfamily=fontfamily, textalign=textalign))
    return resp


@lab3.route('/lab3/clear_cookie')
def clear_cookie():
    resp = make_response(redirect('/lab3/settings/'))
    resp.delete_cookie('color')
    resp.delete_cookie('bgcolor')
    resp.delete_cookie('fsize')
    resp.delete_cookie('textalign')
    return resp


@lab3.route('/lab3/form2/')
def form2():
    errors = {}
    pass_name = request.args.get('pass_name')
    if pass_name == '':
        errors['pass_name'] = 'Заполните поле!'

    shelf = request.args.get('shelf')
    bedding = request.args.get('bedding') == 'on'
    luggage = request.args.get('luggage') == 'on'
    
    age = request.args.get('age')
    if age == None:
        errors['age'] = ''
    elif age =='':
        errors['age'] = 'Заполните поле!'
    else:
        age = int(age)
        if age < 1 or age > 120:
            errors['age'] = 'Возраст должен быть от 1 до 120 лет!'

    departure = request.args.get('departure')
    if departure == '':
        errors['departure'] = 'Заполните поле!'

    destination = request.args.get('destination')
    if destination == '':
        errors['destination'] = 'Заполните поле!'

    date = request.args.get('date')
    if date == '':
        errors['date'] = 'Заполните поле!'
    
    insurance = request.args.get('insurance') == 'on'

    # Устанавливаем цену в шаблоне
    if 'age' in errors:
        price = 0
        ticket_type = ''
    else:
        if age >= 18:
            base_price = 1000
            ticket_type = 'Взрослый билет'
        else:
            base_price = 700
            ticket_type = 'Детский билет'

        if shelf in ['lower', 'lower_side']:
            base_price += 100
        if bedding:
            base_price += 75
        if luggage:
            base_price += 250
        if insurance:
            base_price += 150

        price = base_price

    return render_template('lab3/form2.html', 
                           errors=errors, 
                           pass_name=pass_name, 
                           shelf=shelf,
                           bedding=bedding, 
                           luggage=luggage, 
                           age=age, 
                           departure=departure,
                           destination=destination, 
                           date=date, 
                           insurance=insurance, 
                           ticket_type=ticket_type, 
                           price=price)


products = [
    {"name": "iPhone 14", "price": 999, "color": "Black", "brand": "Apple"},
    {"name": "Samsung Galaxy S21", "price": 799, "color": "Phantom Gray", "brand": "Samsung"},
    {"name": "Google Pixel 6", "price": 599, "color": "Stormy Black", "brand": "Google"},
    {"name": "OnePlus 9", "price": 729, "color": "Morning Mist", "brand": "OnePlus"},
    {"name": "Xiaomi Mi 11", "price": 749, "color": "Horizon Blue", "brand": "Xiaomi"},
    {"name": "Sony Xperia 1", "price": 1299, "color": "Black", "brand": "Sony"},
    {"name": "Nokia G50", "price": 299, "color": "Navy", "brand": "Nokia"},
    {"name": "Oppo Find X3", "price": 1149, "color": "Gloss Black", "brand": "Oppo"},
    {"name": "Vivo X60", "price": 799, "color": "Midnight Black", "brand": "Vivo"},
    {"name": "Realme GT", "price": 599, "color": "Dashing Silver", "brand": "Realme"},
    {"name": "Huawei P40", "price": 899, "color": "Silver Frost", "brand": "Huawei"},
]


@lab3.route('/lab3/search')
def search():
    return render_template('lab3/search.html')


@lab3.route('/lab3/result')
def result():
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)

    filtered_products = [
        product for product in products
        if (min_price is None or product['price'] >= min_price) and
           (max_price is None or product['price'] <= max_price)
    ]

    return render_template('lab3/result.html', products=filtered_products)