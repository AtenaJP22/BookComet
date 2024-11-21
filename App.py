from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from a .env file

app = Flask(__name__)


cosmos_uri = os.getenv("COSMOS_URI", "")
if not cosmos_uri:
    raise ValueError("COSMOS_URI is not set. Add it to your .env file.")

client = MongoClient(cosmos_uri)
db = client["bookstore"]
books_collection = db["books"]


@app.route('/')
def index():
    # Fetch and display all books
    books = books_collection.find()
    return render_template('index.html', books=books)

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        # Get book details from the form
        isbn = request.form['isbn']
        title = request.form['title']
        year = request.form['year']
        price = request.form['price']
        page = request.form['page']
        category = request.form['category']
        cover_photo = request.form['coverphoto']
        publisher_location = request.form['publisher_location']
        publisher_name = request.form['publisher_name']
        author_name = request.form['author_name']

        # Insert the new book into the database
        books_collection.insert_one({
            'isbn': isbn,
            'title': title,
            'year': year,
            'price': price,
            'page': page,
            'category': category,
            'coverPhoto': cover_photo,
            'publisher': {'location': publisher_location, 'name': publisher_name},
            'author': {'name': author_name}
        })

        return redirect(url_for('index'))

    return render_template('add_book.html')

@app.route('/book/<isbn>')
def book_details(isbn):
    # Fetch and display details of a specific book
    book = books_collection.find_one({'isbn': isbn})
    return render_template('book_details.html', book=book)


from flask import render_template, request, redirect, url_for, jsonify

@app.route('/update_book/<isbn>', methods=['GET', 'POST'])
def update_book(isbn):
    book = books_collection.find_one({'isbn': isbn})

    if not book:
        return jsonify({"error": "Book not found"}), 404

    if request.method == 'POST':
        try:
            # Get updated book price from the form
            updated_price = request.form.get('price')

            # Validate and update the book price in the database
            if updated_price is not None and updated_price.replace('.', '', 1).isdigit():
                updated_price = float(updated_price)

                # Update the book price in the database
                books_collection.update_one({'isbn': isbn}, {'$set': {'price': updated_price}})
            
                return redirect(url_for('book_details', isbn=isbn))

            else:
                error_message = "Invalid input. Please enter a valid numeric value for Price."
                return render_template('update_book.html', book=book, error_message=error_message)

        except ValueError:
            error_message = "Invalid input. Please enter a valid numeric value for Price."
            return render_template('update_book.html', book=book, error_message=error_message)

    return render_template('update_book.html', book=book)




@app.route('/delete_book/<isbn>', methods=['GET', 'POST'])
def delete_book(isbn):
    if request.method == 'POST':
        # Delete a specific book by ISBN
        result = books_collection.delete_one({'isbn': isbn})
        if result.deleted_count > 0:
            return redirect(url_for('index'))  # Redirect to index after successful deletion
        else:
            return jsonify({"error": "Book not found"}), 404  # Return JSON response for error

    # If it's a GET request, you can add additional logic if needed
    return render_template('delete_book.html', isbn=isbn)

if __name__ == '__main__':
    app.run(debug=True, port=5001)