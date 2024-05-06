from flask import *
import json

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.errorhandler(404)
def not_found(error):
    if request.path.startswith('/api/'):
        return jsonify({'error': 'url not found'}), 404
    else:
        return "Страница не найдена", 404



@app.route('/api/books')
def get_books():
    with open('books.json', encoding="utf-8") as book_file:
        books = json.load(book_file)
    return books


@app.route('/api/books', methods=['POST'])
def create_book():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['title', 'author']):
        return jsonify({'error': 'Bad request'})
    with open('books.json', encoding="utf-8") as book_file:
        books = json.load(book_file)
    books["books"].append(request.json)
    with open("books.json", 'w', encoding="utf-8") as file:
        json.dump(books,file, ensure_ascii = False,indent = 2)
    return jsonify({'success': 'OK'})

if __name__ == '__main__':
    app.run(debug=True)