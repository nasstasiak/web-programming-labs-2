from flask import render_template, Blueprint, request, redirect, url_for, session

lab9 = Blueprint('lab9', __name__)


@lab9.route('/lab9/', methods=['GET', 'POST'])
def form_name():
    errors = {}

    # Проверяем, есть ли сохранённые данные в сессии
    if 'user' in session:
        return redirect(url_for('lab9.form_congrats'))

    user = request.form.get('user')  # Используем request.form для POST-запросов
    
    if request.method == 'POST':
        if not user:
            errors['user'] = 'Заполните поле "Имя"'
        else:
            session['user'] = user  # Сохраняем имя в сессии
            return redirect(url_for('lab9.form_age'))

    return render_template('/lab9/lab9.html', user=user, errors=errors)


@lab9.route('/lab9/age/', methods=['GET', 'POST'])
def form_age():
    errors = {}
    user = session.get('user')  # Получаем имя из сессии
    age = request.form.get('age')  # Получаем возраст из формы

    if request.method == 'POST':
        if not age:
            errors['age'] = 'Заполните поле "Возраст"'
        else:
            session['age'] = age  # Сохраняем возраст в сессии
            return redirect(url_for('lab9.form_gender'))

    return render_template('/lab9/age.html', user=user, age=age, errors=errors)


@lab9.route('/lab9/gender/', methods=['GET', 'POST'])
def form_gender():
    errors = {}
    user = session.get('user')
    age = session.get('age')
    gender = request.form.get('gender')

    if request.method == 'POST':
        if not gender:
            errors['gender'] = 'Заполните поле "Пол"'
        else:
            session['gender'] = gender  # Сохраняем пол в сессии
            return redirect(url_for('lab9.form_preference'))

    return render_template('/lab9/gender.html', user=user, age=age, gender=gender, errors=errors)


@lab9.route('/lab9/preference/', methods=['GET', 'POST'])
def form_preference():
    errors = {}
    user = session.get('user')
    age = session.get('age')
    gender = session.get('gender')
    preference = request.form.get('preference')

    if request.method == 'POST':
        if not preference:
            errors['preference'] = 'Выберите один из вариантов'
        else:
            session['preference'] = preference  # Сохраняем предпочтение в сессии
            return redirect(url_for('lab9.form_detail'))

    return render_template('/lab9/preference.html', user=user, age=age, gender=gender, errors=errors)


@lab9.route('/lab9/detail/', methods=['GET', 'POST'])
def form_detail():
    errors = {}
    user = session.get('user')
    age = session.get('age')
    gender = session.get('gender')
    preference = session.get('preference')
    detail = request.form.get('detail')

    if preference == 'вкусное':
        options = [('сладкое', 'Сладкое'), ('соленое', 'Соленое')]
    elif preference == 'красивое':
        options = [('большое', 'Большое'), ('маленькое', 'Маленькое')]
    else:
        options = []

    if request.method == 'POST':
        if not detail:
            errors['detail'] = 'Выберите один из вариантов'
        else:
            session['detail'] = detail  # Сохраняем детали в сессии
            return redirect(url_for('lab9.form_congrats'))

    return render_template('/lab9/detail.html', user=user, age=age, gender=gender, preference=preference, options=options, errors=errors)


@lab9.route('/lab9/congrats/', methods=['GET'])
def form_congrats():
    user = session.get('user')
    age = int(session.get('age'))
    gender = session.get('gender')
    preference = session.get('preference')
    detail = session.get('detail')

    # Определяем поздравление и картинку
    if gender == 'male':
        if age < 18:
            if preference == 'вкусное':
                if detail == 'сладкое':
                    message = f"Поздравляю, {user}! Пусть твоя жизнь будет яркой и сладкой, как эти конфеты!  Вот тебе сладкий подарок!"
                    image = "candy.png"
                elif detail == 'соленое':
                    message = f"Поздравляю, {user}!  Желаю тебе энергии и задора, как от этих хрустящих чипсов! Вот тебе вкусный сюрприз!"
                    image = "chips.png"
            elif preference == 'красивое':
                if detail == 'большое':
                    message = f"Поздравляю, {user}!  Пусть твоя жизнь будет такой же мощной и впечатляющей, как эта машина! Вот тебе крутая модель!"
                    image = "big_toy_car.png"
                elif detail == 'маленькое':
                    message = f"Поздравляю, {user}! Желаю тебе  удачи и стиля, как у этой миниатюрной машинки! Вот тебе стильный подарок!"
                    image = "small_toy_car.png"
        else:  # Старше 18 лет
            if preference == 'вкусное':
                if detail == 'сладкое':
                    message = f"Поздравляем, {user}!  Пусть жизнь будет сладкой и приятной, как эти изысканные конфеты! Вот тебе сладкий подарок!"
                    image = "candy.png"
                elif detail == 'соленое':
                    message = f"Поздравляем, {user}! Желаем вам насыщенной и яркой жизни, полной незабываемых моментов, как вкус этих чипсов! Вот тебе  подарок!"
                    image = "chips.png"
            elif preference == 'красивое':
                if detail == 'большое':
                    message = f"Поздравляем, {user}!  Желаем вам  успеха и стиля, как у этого роскошного автомобиля! Вот тебе стильный подарок!"
                    image = "big_car.png"
                elif detail == 'маленькое':
                    message = f"Поздравляем, {user}! Пусть в вашей жизни всегда будет место для маленьких радостей! Вот тебе очаровательный подарок!"
                    image = "small_car.png"
    elif gender == 'female':
        if age < 18:
            if preference == 'вкусное':
                if detail == 'сладкое':
                    message = f"Поздравляю, {user}! Пусть твоя жизнь будет такой же сладкой и волшебной, как эти конфеты! Вот тебе сладкий подарок!"
                    image = "candy.png"
                elif detail == 'соленое':
                    message = f"Поздравляю, {user}!  Желаю тебе  энергии и  хорошего настроения, как от этих чипсов! Вот тебе вкусный сюрприз!"
                    image = "chips.png"
            elif preference == 'красивое':
                if detail == 'большое':
                    message = f"Поздравляю, {user}! Пусть твоя жизнь будет такой же яркой и блестящей, как это украшение! Вот тебе прекрасный подарок!"
                    image = "girl_jewelry.png"
                elif detail == 'маленькое':
                    message = f"Поздравляю, {user}! Желаем тебе  уютной и счастливой жизни, как от этого милого украшения! Вот тебе замечательный подарок!"
                    image = "girl_mini_jewelry.png"
        else:  # Старше 18 лет
            if preference == 'вкусное':
                if detail == 'сладкое':
                    message = f"Поздравляем, {user}! Пусть ваша жизнь будет наполнена радостью и удовольствием, как вкус этих конфет! Вот тебе  сладкий подарок!"
                    image = "candy.png"
                elif detail == 'соленое':
                    message = f"Поздравляем, {user}!  Желаем вам ярких впечатлений и незабываемых моментов, как от вкуса этих чипсов! Вот тебе  подарок!"
                    image = "chips.png"
            elif preference == 'красивое':
                if detail == 'большое':
                    message = f"Поздравляем, {user}!  Пусть вам жизнь будет такой же роскошной и впечатляющей, как это украшение! Вот тебе  прекрасный подарок!"
                    image = "jewelry.png"
                elif detail == 'маленькое':
                    message = f"Поздравляем, {user}! Пусть ваша жизнь будет наполнена маленькими радостями и очарованием! Вот тебе замечательный подарок!"
                    image = "mini_jewelry.png"

    # Сохраняем данные в сессию
    session['message'] = message
    session['image'] = image

    return render_template('/lab9/congrats.html', user=user, message=message, image=image)


@lab9.route('/lab9/reset', methods=['GET'])
def reset():
    session.clear()  # Очищаем всю сессию
    return redirect(url_for('lab9.form_name'))