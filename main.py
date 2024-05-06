from flask import Flask, render_template, request, redirect, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Book
from flask_restful import reqparse, abort, Api, Resource
import json


app = Flask(__name__)
api = Api(app)

# Подключаемся и создаем сессию базы данных
engine = create_engine('sqlite:///books-collection.db?check_same_thread=False', echo=True)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


def abort_if_book_not_found(book_id):
    book = session.query(Book).get(book_id)
    if not book:
        abort(404, message=f"Book {book_id} not found")

class BookResource(Resource):
    def get(self, book_id):
        abort_if_book_not_found(book_id)
        book = session.query(Book).get(book_id)
        return jsonify(
            {
                'book': book.to_dict(only=('id', 'title', 'author', 'genre'))
            })

    def delete(self, book_id):
        abort_if_book_not_found(book_id)
        book = session.query(Book).get(book_id)
        session.delete(book)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, book_id):
        abort_if_book_not_found(book_id)
        book = session.query(Book).get(book_id)
        if not request.json:
            return jsonify({'error': 'Empty request'})
        data = request.json
        if 'title' in request.json:
            book.title = data['title']
        if 'author' in request.json:
            book.author = data['author']
        if 'genre' in request.json:
            book.genre = data['genre']
        session.add(book)
        session.commit()
        return jsonify({'success': 'OK'})

class BooksResource(Resource):
    def get(self):
        books = session.query(Book).all()
        return jsonify(
            {
                'books': [book.to_dict(only=('id', 'title', 'author', 'genre')) for book in books]
            })


# страница, которая будет отображать все книги в базе данных
# Эта функция работает в режиме чтения.
@app.route('/')
@app.route('/books')
def showBooks():
    books = session.query(Book).all()
    return render_template("books.html", books=books)


# Эта функция позволит создать новую книгу и сохранить ее в базе данных.
@app.route('/books/new/', methods=['GET', 'POST'])
def newBook():
    if request.method == 'POST':
        newBook = Book(title=request.form['name'], author=request.form['author'],
                       genre=request.form['genre'])
        session.add(newBook)
        session.commit()
        return redirect(url_for('showBooks'))
    else:
        return render_template('newBook.html')

    # Эта функция позволит нам обновить книги и сохранить их в базе данных.


@app.route("/books/<int:book_id>/edit/", methods=['GET', 'POST'])
def editBook(book_id):
    editedBook = session.query(Book).filter_by(id=book_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedBook.title = request.form['name']
        if request.form['author']:
            editedBook.author = request.form['author']
        if request.form['genre']:
            editedBook.genre = request.form['genre']
        session.add(editedBook)
        session.commit()
        return redirect(url_for('showBooks'))
    else:
        return render_template('editBook.html', book=editedBook)

    # Эта функция для удаления книг


@app.route('/books/<int:book_id>/delete/', methods=['GET', 'POST'])
def deleteBook(book_id):
    bookToDelete = session.query(Book).filter_by(id=book_id).one()
    if request.method == 'POST':
        session.delete(bookToDelete)
        session.commit()
        return redirect(url_for('showBooks', book_id=book_id))
    else:
        return render_template('deleteBook.html', book=bookToDelete)

api.add_resource(BookResource, '/api/books/<int:book_id>')
api.add_resource(BooksResource, '/api/books')

app.run(debug=True)