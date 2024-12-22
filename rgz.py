from flask import Blueprint, request, jsonify, session, redirect, url_for, render_template
from flask_login import login_user, logout_user, login_required, current_user
from db import db
from db.models import users, Book


rgz = Blueprint('rgz', __name__)

# Главная страница со списком книг
@rgz.route('/rgz/')
def rgz_page():
    return render_template('rgz/rgz.html')

# Страница входа
@rgz.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_name = request.form['login']
        password = request.form['password']

        # Проверка на администратора
        if login_name == 'Admin' and password == 'root':
            session['login'] = login_name  # Сохраняем логин в сессии
            return redirect(url_for('rgz.admin_books'))
        else:
            # Возвращаем JSON-ответ с сообщением об ошибке
            return jsonify({
                'error': 'Извините, вы не являетесь администратором'
            }), 403

    return render_template('rgz/login.html')

# Страница администрирования
@rgz.route('/admin')
def admin_books():
    if not session.get('login') == 'Admin':
        return redirect(url_for('rgz.login'))

    return render_template('rgz/admin.html')

# API JSON-RPC
@rgz.route('/rgz/json-rpc-api/', methods=['POST'])
def api():
    data = request.json
    id = data.get('id')

    # Метод для получения списка книг
    if data['method'] == 'get_books':
        books = Book.query.all()
        return {
            'jsonrpc': '2.0',
            'result': [{
                'id': book.id,
                'title': book.title,
                'author': book.author,
                'pages': book.pages,
                'publisher': book.publisher,
                'cover_image': book.cover_image
            } for book in books],
            'id': id
        }

    # Метод для добавления книги
    if data['method'] == 'add_book':
        params = data.get('params')
        if not params:
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': -32602,
                    'message': 'Invalid params'
                },
                'id': id
            }

        title = params.get('title')
        author = params.get('author')
        pages = params.get('pages')
        publisher = params.get('publisher')
        cover_image = params.get('cover_image')

        if not title or not author or not pages or not publisher or not cover_image:
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': -32602,
                    'message': 'All fields are required'
                },
                'id': id
            }

        new_book = Book(
            title=title,
            author=author,
            pages=pages,
            publisher=publisher,
            cover_image=cover_image
        )
        db.session.add(new_book)
        db.session.commit()
        return {
            'jsonrpc': '2.0',
            'result': 'success',
            'id': id
        }

    # Метод для удаления книги
    if data['method'] == 'delete_book':
        params = data.get('params')
        if not params:
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': -32602,
                    'message': 'Invalid params'
                },
                'id': id
            }

        book_id = params.get('id')
        if not book_id:
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': -32602,
                    'message': 'Book ID is required'
                },
                'id': id
            }

        book = Book.query.get(book_id)
        if not book:
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': -32602,
                    'message': 'Book not found'
                },
                'id': id
            }

        db.session.delete(book)
        db.session.commit()
        return {
            'jsonrpc': '2.0',
            'result': 'success',
            'id': id
        }

    # Метод для редактирования книги
    if data['method'] == 'edit_book':
        params = data.get('params')
        if not params:
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': -32602,
                    'message': 'Invalid params'
                },
                'id': id
            }

        book_id = params.get('id')
        title = params.get('title')
        author = params.get('author')
        pages = params.get('pages')
        publisher = params.get('publisher')
        cover_image = params.get('cover_image')

        if not book_id or not title or not author or not pages or not publisher or not cover_image:
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': -32602,
                    'message': 'All fields are required'
                },
                'id': id
            }

        book = Book.query.get(book_id)
        if not book:
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': -32602,
                    'message': 'Book not found'
                },
                'id': id
            }

        # Обновляем данные книги
        book.title = title
        book.author = author
        book.pages = pages
        book.publisher = publisher
        book.cover_image = cover_image
        db.session.commit()
        return {
            'jsonrpc': '2.0',
            'result': 'success',
            'id': id
        }

    return {
        'jsonrpc': '2.0',
        'error': {
            'code': -32601,
            'message': 'Method not found'
        },
        'id': id
    }
