from flask import Blueprint, render_template, request, make_response, redirect, url_for
lab3 = Blueprint('lab3', __name__)


@lab3.route('/lab3/')
def lab():
    name = request.cookies.get('name')
    name_color = request.cookies.get('name_color')
    return render_template('lab3/lab3.html', name= name, name_color = 'name_color')


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


@lab3.route('/lab3/form2/')
def form2():
    errors = {}

    user = request.args.get('user')

    if user == '':
        errors ['user'] = 'Заполните поле "Имя"'

    age = request.args.get('age')

    if age is None:
        errors['age'] = ''#excluding typeerror
    
    elif age == '':
        errors['age'] = 'Заполните поле "Возраст"'
    else:
        try:
            age = int(age)
            if age < 1 or age > 120:
                errors['age'] = 'Возраст должен быть от 1 до 120 лет'
        except ValueError:
            errors['age'] = 'Возраст должен быть числом'

    departure = request.args.get('departure')

    if departure == '':
        errors ['departure'] = 'Заполните поле "Пункт отправления"'

    destination = request.args.get('destination')

    if destination == '':
        errors['destination'] = 'Заполните поле "Пункт назначения"'

    date = request.args.get('date')

    if date == '':
        errors['date'] = 'Заполните поле "Дата поездки"'

    berth = request.args.get('berth')
    baggage = request.args.get('baggage') == 'on'
    linen = request.args.get('linen') == 'on'
    insurance = request.args.get('insurance') == 'on'

    return render_template('/lab3/form2.html', 
                           user=user, 
                           age=age, 
                           departure=departure, 
                           destination=destination, 
                           date=date, 
                           berth=berth, 
                           baggage=baggage, 
                           linen=linen, 
                           insurance=insurance, 
                           errors=errors)




