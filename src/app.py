from flask import Flask, jsonify, request, render_template
from config import config_data as config
from flask_sqlalchemy import SQLAlchemy
import psycopg

DEBUG = False
HOST = "127.0.0.1" if DEBUG else "0.0.0.0"

# Initialize the Flask app
app = Flask(__name__)

# Configure global application data 
app_data = {}
app_data['app_name'] = config['app_name']
app_data['interface'] = config['interface']

# Configure the database
db_username = config['db_username']
db_password = config['db_password']
db_host = config['db_host']
db_port = config['db_port']
db_name = config['db_name']
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Define the database model
class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f"<Book {self.title} by {self.author}>"

# Load SQL before app runs
def load_sql():
    try:
        sql_file_path = './sql/schema.sql'
        with open(sql_file_path, 'r') as file:
            sql_script = file.read()
        with psycopg.connect(
            dbname=db_name,
            user=db_username,
            password=db_password,
            host=db_host,
            port=db_port
        ) as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql_script)
                conn.commit()
        print("SQL script executed successfully.")
    except Exception as e:
        print(f"Error executing SQL script: {e}")

# Initialize the database and load the SQL before the app starts
with app.app_context():
    # Drop everything in the database to avoid duplication
    db.drop_all()
    # Load SQL and manually create tables before the app runs
    load_sql()
    '''
    # Instead of load_sql(), you could also do the following:

    # 1) Create tables based on the ORM models
    db.create_all()

    # 2) Add an item to the database
    books = [
        Books(title='The Linux Command Line', author='William Shotts'),
        Books(title='The Mythical Man-Month', author='Frederick P. Brooks Jr.'),
        Books(title='Press Reset', author='Jason Schreier'),
        Books(title='How to code Snake in Python', author='Len Feremans'),
        Books(title='Blood, Sweat, and Pixels', author='Jason Schreier')
    ]

    db.session.add_all(books)
    db.session.commit()
    '''

############
# REST API #
############

# Endpoint to retrieve all books (optionally filter by author)
@app.route('/books', methods=['GET'])
def get_books():
    query = Books.query

    # Optional filter (/books?author=Jason Schreier)
    author = request.args.get('author')
    if author:
        # Case-insensitive partial match
        query = query.filter(Books.author.ilike(f"%{author}%"))

    books = query.all()
    return jsonify([
        {'id': b.id, 'title': b.title, 'author': b.author} for b in books
    ])

# Endpoint to retrieve a book by its ID
@app.route('/books/<int:id>', methods=['GET'])
def get_books_id(id):
    book = Books.query.get(id)
    if book:
        return jsonify({
            'id': book.id,
            'title': book.title,
            'author': book.author
        })
    else:
        return jsonify({'message': 'Book not found'}), 404

# Endpoint to add a new book
@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json(silent=True)

    # Fallback to form data if JSON is not found
    if data is None:
        data = {
            "title": request.form.get("title"),
            "author": request.form.get("author")
        }

    book_title = data.get('title')
    book_author = data.get('author')

    # Create and save new book
    new_book = Books(title=book_title, author=book_author)
    db.session.add(new_book)
    db.session.commit()
    return jsonify({'message': 'Book added successfully'}), 201

# Endpoint to delete a book by ID
@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = Books.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'Book deleted successfully'})

########
# VIEW #
########

# Home route (renders index page)
@app.route('/')
def index(): 
    app_data['interface'] = ""
    return render_template('index.html', app_data=app_data)

# Server-Side Rendered HTML views using different UI frameworks
@app.route("/ssr/classic")
def show_classic():
    app_data['interface'] = "(pure html/classic)"

    books = Books.query.all()
    books_data = [{'id': b.id, 'title': b.title, 'author': b.author} for b in books]
    # Render quote_objects "server-side" using Jinja 2 template system
    return render_template('classic.html', app_data=app_data, books=books_data)

@app.route("/ssr/ajax")
def show_quotes_ajax():
    app_data['interface'] = "(ajax)"
    # Render quote_objects "server-side" using Jinja 2 template system
    return render_template('ajax.html', app_data=app_data)

@app.route("/ssr/react")
def show_quotes_react():
    app_data['interface'] = "(react)"
    # Render quote_objects "server-side" using Jinja 2 template system
    return render_template('react.html', app_data=app_data)

@app.route("/ssr/vue")
def show_quotes_vue():
    app_data['interface'] = "(vue)"
    # Render quote_objects "server-side" using Jinja 2 template system
    return render_template('vue.html', app_data=app_data)

##################
# RUN DEV SERVER #
##################
if __name__ == "__main__":
    app.run(HOST, debug=DEBUG)