# . venv/Scripts/activate

import sqlite3

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, fetch_book_details_from_google

import re

def strip_tags(text):
    """Remove HTML tags from a given string."""
    return re.sub(r'<[^>]*>', '', text)


# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.jinja_env.filters['strip_tags'] = strip_tags

class Database:
    def __init__(self, database):
        self.database = database

    def get_conn(self):
        conn = sqlite3.connect(self.database)
        conn.row_factory = sqlite3.Row  # Set row factory to sqlite3.Row
        return conn

    def execute(self, query, params=None):
        params = params or []
        with self.get_conn() as conn:  # This ensures connection is closed after the block
            cur = conn.cursor()
            cur.execute(query, params)
            if query.strip().upper().startswith('SELECT'):
                return cur.fetchall()
            else:
                conn.commit()
                return cur.lastrowid

    def commit(self):
        with self.get_conn() as conn:
            conn.commit()

    def rollback(self):
        with self.get_conn() as conn:
            conn.rollback()

            
# Configure CS50 Library to use SQLite database
db = Database("E:/Desktop/Study/Final Project/books_reviews.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user FIRST"""
    # forget any user_id
    session.clear()

    # POST
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Ensure username was submitted
        if not username:
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not password:
            return apology("must provide password", 400)

        # Ensure confirmation was submitted
        elif not confirmation:
            return apology("must confirm password", 400)

        # Ensure password and confirmation match
        elif password != confirmation:
            return apology("passwords do not match", 400)

        # query and check if username exist
        rows = db.execute("SELECT * FROM users WHERE username =?", (username,))
        if len(rows) != 0:
            return apology("username already exists", 400)

        # insert new user into db
        db.execute("INSERT INTO users (username, password_hash) VALUES(?, ?)", (username, generate_password_hash(password)))

        # query and remember user of this session
        rows = db.execute("SELECT * FROM users WHERE username =?", (username,))
        session["user_id"] = rows[0]["user_id"]

        # redirect to homepage
        return redirect("/")

    # get
    else:
        return render_template("register.html")
    

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        # Ensure username was submitted
        if not username:
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not password:
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["password_hash"], password
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["user_id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")
    
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/results", methods=["GET"])
@login_required
def results():
    title = request.args.get("title")
    author = request.args.get("author")
    isbn = request.args.get("isbn")
    publisher = request.args.get("publisher")
    query = ''
    page = request.args.get('page', 1, type=int)
    start_index = (page - 1) * 10  # Assuming 10 results per page

    if title:
        query += f'intitle:{title}'
    if author:
        if query:  # Add AND if there's already part of the query
            query += ' AND '
        query += f'inauthor:{author}'
    if isbn:
        if query:
            query += ' AND '
        query += f'isbn:{isbn}'
    if publisher:
        if query:
            query += ' AND '
        query += f'publisher:{publisher}'

    books = lookup(query, start_index=start_index)
    return render_template('results.html', books=books, current_page=page, title=title, author=author, isbn=isbn, publisher=publisher, query=query)


@app.route("/")
@login_required
def index():
    return render_template("index.html")


@app.route("/my_library", methods=["GET"])
@login_required
def my_library():
    user_id = session.get('user_id')
    print("User ID:", user_id)  # Debug: Confirm user ID
    books = db.execute("SELECT b.* FROM books b JOIN user_books ub ON b.book_id = ub.book_id WHERE ub.user_id = ?", (user_id,))
    print("Books fetched:", books)  # Debug: Review fetched books
    return render_template('my_library.html', books=books)


import logging

logging.basicConfig(level=logging.DEBUG)

@app.route("/add_book_to_library", methods=["POST"])
@login_required
def add_book_to_library():
    user_id = session.get('user_id')
    book_id = request.form.get('book_id')
    if not book_id:
        flash("Book ID is missing!", "error")
        return redirect(url_for('index'))

    # Check if book is already in the database
    existing_book = db.execute("SELECT * FROM books WHERE book_id = ?", (book_id,))
    if not existing_book:
        book_details = fetch_book_details_from_google(book_id)
        if book_details:
            db.execute("INSERT INTO books (book_id, title, author, publisher, publish_date, description, cover_image_url) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (book_details['book_id'], book_details['title'], book_details['author'], book_details['publisher'], 
                        book_details['publish_date'], book_details['description'], book_details['cover_image_url']))

    # Add book to user's library
    try:
        db.execute("INSERT INTO user_books (user_id, book_id) VALUES (?, ?)", (user_id, book_id))
        db.commit()
        flash("Book added to your library successfully!", "success")
    except Exception as e:
        db.rollback()
        flash(f"Failed to add book to library: {str(e)}", "error")

    return redirect(url_for('my_library'))


@app.route("/book_details/<book_id>")
@login_required
def book_details(book_id):
    # Fetch book details from the database or an external API
    book = db.execute("SELECT * FROM books WHERE book_id = ?", (book_id,))
    if not book:
        flash("Book not found.", "error")
        return redirect(url_for('my_library'))
    return render_template('book_details.html', book=book[0])
