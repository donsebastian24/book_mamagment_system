from flask import Flask, render_template, request, redirect, jsonify, send_file, url_for
import sqlite3
import csv
import io
from flask_login import login_required
from login import app  # Ensure this is importing correctly


# Database connection function
def connect_db():
    conn = sqlite3.connect('books.db')
    return conn

def get_books(page, per_page):
    conn = connect_db()
    conn.row_factory = sqlite3.Row
    offset = (page - 1) * per_page
    cursor = conn.execute("SELECT Title, Author FROM inventory LIMIT ? OFFSET ?", (per_page, offset))
    books = cursor.fetchall()
    conn.close()
    return books


@app.route('/')

def index():
    page = request.args.get('page', 1, type=int)  # Get current page from query parameter
    per_page = 5  # Number of books per page

    books = get_books(page, per_page)

    # Count total books to calculate total pages
    with connect_db() as conn:
        cursor = conn.execute("SELECT COUNT(*) FROM inventory")
        total_books = cursor.fetchone()[0]
        total_pages = (total_books + per_page - 1) // per_page  # Calculate total pages

    return render_template('index.html', books=books, page=page, total_pages=total_pages)


@app.route('/search_results')
@login_required
def search_results():
    # Get the search query from the URL
    search_query = request.args.get('query', '').strip()

    if not search_query:
        # If no search query is provided, redirect back to the main page or show all books
        return redirect(url_for('index'))

    # Use a wildcard for searching similar entries
    like_query = f'%{search_query}%'

    # SQL query to search for the query in title, author, or publication year
    query = """
    SELECT id, title, author, genre, publication_date, isbn, category
    FROM inventory
    WHERE title LIKE ? OR author LIKE ? OR strftime('%Y', publication_date) LIKE ?
    """

    filters = (like_query, like_query, like_query)

    with connect_db() as conn:
        cur = conn.cursor()
        cur.execute(query, filters)
        search_results = cur.fetchall()

    # Render the search results in the 'view_books.html' template
    return render_template('view_books.html', books=search_results, search_query=search_query)


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        genre = request.form['genre']
        publication_date = request.form['publication_date']
        isbn = request.form['isbn']
        category = request.form['category']

        with connect_db() as conn:
            conn.execute(
                "INSERT INTO inventory (title, author, genre, publication_date, isbn, category) VALUES (?, ?, ?, ?, ?, ?)",
                (title, author, genre, publication_date, isbn, category))
            conn.commit()

        return redirect('/')  # Redirect to the index page

    return render_template('add_book.html')


@app.route('/category/<category_name>', methods=['GET'])
@login_required
def category(category_name):
    with connect_db() as conn:
        cursor = conn.execute("SELECT * FROM inventory WHERE category = ?", (category_name,))
        books = cursor.fetchall()
    return render_template('category.html', category=category_name, books=books)


# Route to render the export page for CSV
@app.route('/export_csv.html')
@login_required
def export_csv_page():
    return render_template('export_csv.html')


# Route to render the export page for JSON
@app.route('/export_json.html')
@login_required
def export_json_page():
    return render_template('export_json.html')


@app.route('/export_csv', methods=['GET'])
@login_required
def export_csv():
    category = request.args.get('category')
    author = request.args.get('author')
    year = request.args.get('year')
    bulk_export = request.args.get('bulk_export')  # Check if bulk export is requested

    # Build the SQL query dynamically based on filters
    query = "SELECT * FROM inventory WHERE 1=1"
    filters = []

    if bulk_export and bulk_export.lower() == 'true':
        # If bulk export, do not apply any filters, export all records
        print("Bulk export requested")
    else:
        # Apply filters if not bulk export
        if category:
            query += " AND category LIKE ?"
            filters.append(f"%{category}%")
        if author:
            query += " AND author LIKE ?"
            filters.append(f"%{author}%")
        if year:
            query += " AND strftime('%Y', publication_date) = ?"
            filters.append(year)

    print(f"Final SQL Query: {query}")
    print(f"Filters Applied: {filters}")

    # Execute the query
    with connect_db() as conn:
        cursor = conn.execute(query, filters)
        books = cursor.fetchall()

    print(f"Number of records fetched: {len(books)}")

    # Prepare CSV output
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Title', 'Author', 'Genre', 'Publication Date', 'ISBN', 'Category'])  # Column headers
    writer.writerows(books)  # Write all rows

    # Return CSV as downloadable file
    output.seek(0)  # Go to the start of the StringIO buffer
    return send_file(io.BytesIO(output.getvalue().encode()), download_name='books.csv', as_attachment=True)


@app.route('/export_json', methods=['GET'])
@login_required
def export_json():
    category = request.args.get('category')
    author = request.args.get('author')
    year = request.args.get('year')

    # Build the SQL query dynamically based on filters
    query = "SELECT * FROM inventory WHERE 1=1"
    filters = []

    if category:
        query += " AND category LIKE ?"
        filters.append(f"%{category}%")
    if author:
        query += " AND author LIKE ?"
        filters.append(f"%{author}%")
    if year:
        query += " AND strftime('%Y', publication_date) = ?"
        filters.append(year)

    with connect_db() as conn:
        cursor = conn.execute(query, filters)
        books = cursor.fetchall()

    books_json = [
        {'id': book[0], 'title': book[1], 'author': book[2], 'genre': book[3], 'publication_date': book[4],
         'isbn': book[5], 'category': book[6]}
        for book in books
    ]
    return jsonify(books_json)




@app.route('/edit_book/<int:book_id>', methods=['GET', 'POST'])
@login_required
def edit_book(book_id):
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        category = request.form['category']
        publication_date = request.form['published_date']  # Match the input name

        # Update the book in the database
        with connect_db() as conn:
            conn.execute("UPDATE inventory SET title = ?, author = ?, category = ?, publication_date = ? WHERE id = ?",
                         (title, author, category, publication_date, book_id))
            conn.commit()

        return redirect(url_for('category', category_name=category))  # Redirect to the category page after editing

    # If the request method is GET, fetch the current details of the book to prepopulate the form
    with connect_db() as conn:
        cursor = conn.execute("SELECT * FROM inventory WHERE id = ?", (book_id,))
        book = cursor.fetchone()

    return render_template('edit_book.html', book=book)  # Pass the book to the template


@app.route('/remove_book/<int:book_id>', methods=['POST'])
@login_required
def remove_book(book_id):
    # Ensure you capture the category name from the request
    category_name = request.form.get('category_name')  # Get the category name from the form

    if not category_name:
        # If category_name is not provided, handle this case
        return redirect(url_for('home'))  # Redirect to a default page or handle it as necessary

    # Proceed to delete the book from the database
    with connect_db() as conn:
        conn.execute("DELETE FROM inventory WHERE id = ?", (book_id,))
        conn.commit()

    # Redirect to the category page with the category_name
    return redirect(url_for('category', category_name=category_name))


if __name__ == '__main__':
    app.run(debug=True)
