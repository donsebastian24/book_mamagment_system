# Book Management System

A simple Flask-based web application to manage a book inventory system. This project allows users to manage books, search for books, view books by category, and export book data in CSV and JSON formats. The system includes a user authentication system using Flask-Login, with login and registration functionality.

## Features

- **User Authentication:**
  - Users can register and log in to access the system.
  - Passwords are securely stored using hashed passwords.
  
- **Book Management:**
  - Add, edit, and delete books from the inventory.
  - View books by category.
  
- **Book Search:**
  - Search books by title, author, or publication year.

- **Data Export:**
  - Export filtered book data as CSV or JSON.

## Requirements

Before running the project, make sure you have the following installed:

- Python 3.x
- Flask
- Flask-Login
- SQLite
- Other dependencies (listed in `requirements.txt`)

To install the necessary Python packages, use the following command:
```bash
pip install -r requirements.txt
Setting Up the Project
1. Clone the repository
bash
Copy code
git clone https://github.com/donsebastian24/book_mamagment_system.git
2. Set Up the Database
Make sure to create an SQLite database (books.db) for the application. You can use the sqlite3 command-line tool or a SQLite GUI to create the books.db file.

The books.db should contain the following tables:

users: For storing user information (username and password).
inventory: For storing book details such as title, author, genre, publication date, ISBN, and category.
You can run the following SQL command to create the necessary tables:

sql
Copy code
-- Create users table
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);

-- Create inventory table
CREATE TABLE inventory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    genre TEXT,
    publication_date DATE,
    isbn TEXT,
    category TEXT
);
3. Running the Application
To run the application, use the following command:

bash
Copy code
python main.py
This will start the Flask development server at http://127.0.0.1:5000.

4. Accessing the Application
Navigate to http://127.0.0.1:5000 in your browser.
Use the Register page to create a new account.
Once registered, log in using the Login page.
Project Structure
php
Copy code
book_management_system/
├── app.py                  # Main Flask application file
├── login.py                # User authentication handling
├── templates/              # HTML templates for rendering views
│   ├── index.html          # Main page showing books
│   ├── add_book.html       # Add book page
│   ├── view_books.html     # Page to view books
│   ├── register.html       # User registration page
│   ├── login.html          # User login page
│   └── ...                 # Other templates
├── static/                 # Static files like CSS, JS, and images
├── requirements.txt        # Python dependencies
├── README.md               # This README file
└── books.db                # SQLite database for books and users
Contributing
If you'd like to contribute to the project, feel free to fork the repository, make changes, and submit a pull request. Please ensure that your code follows proper coding standards and includes tests if applicable.

License
This project is open source and available under the MIT License.

Contact
For any questions or feedback, please reach out to Don Sebastian at donsebastian2421.ca@gmail.com.
