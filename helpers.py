import csv
import datetime
import os
import pytz
import requests
import sqlite3
import urllib
import uuid

from flask import redirect, render_template, request, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


def lookup(query, start_index=0, max_results=10):
    """Search books for its details."""

    # replace 'GOOGLEBook_API_KEY' with your own API key https://console.cloud.google.com/apis/library/browse?project=book-search-421116&q=books%20api
    google_api_key = os.environ.get('GOOGLEBook_API_KEY')

    # Prepare API request
    params = {
        "q": query,
        "startIndex": start_index,
        "maxResults": max_results,
        "key": google_api_key
    }
    
    # Google Book API base url
    url = (
        "https://www.googleapis.com/books/v1/volumes"
    )

    # Query API
    try:
        response = requests.get(
            url,
            params=params
        )
        response.raise_for_status() # Raises an HTTPError if the HTTP request returned an unsuccessful status code
        return response.json()['items']  # Returns a list of book items

    except (KeyError, IndexError,requests.exceptions.HTTPError, requests.RequestException, ValueError):
        return None
    

def fetch_book_details_from_google(book_id):
    """Fetches book details from Google Books API."""
    url = f"https://www.googleapis.com/books/v1/volumes/{book_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises HTTPError for bad responses
        book_data = response.json()
        return {
            'book_id': book_data['id'],
            'title': book_data['volumeInfo'].get('title', ''),
            'author': ', '.join(book_data['volumeInfo'].get('authors', ['Unknown'])),
            'publisher': book_data['volumeInfo'].get('publisher', 'Unknown'),
            'publish_date': book_data['volumeInfo'].get('publishedDate', 'Unknown'),
            'description': book_data['volumeInfo'].get('description', 'No description available.'),
            'cover_image_url': book_data['volumeInfo'].get('imageLinks', {}).get('thumbnail', '')
        }
    except requests.RequestException as e:
        print(f"Request failed: {e}")
    except ValueError as e:
        print(f"JSON decode failed: {e}")
    return None