# Library Management System - Flask Application

from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def connect_db():
    return sqlite3.connect('library.db')

# Initialize Database
def initialize_database():
    conn = connect_db()
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''CREATE TABLE IF NOT EXISTS Books (
        BookID INTEGER PRIMARY KEY AUTOINCREMENT,
        Title TEXT NOT NULL,
        AuthorID INTEGER NOT NULL,
        CategoryID INTEGER NOT NULL,
        ISBN TEXT UNIQUE NOT NULL,
        Availability BOOLEAN DEFAULT 1
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Members (
        MemberID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL,
        Contact TEXT UNIQUE NOT NULL,
        MembershipDate DATE NOT NULL
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Transactions (
        TransactionID INTEGER PRIMARY KEY AUTOINCREMENT,
        BookID INTEGER NOT NULL,
        MemberID INTEGER NOT NULL,
        IssueDate DATE NOT NULL,
        ReturnDate DATE
    )''')

    conn.commit()
    conn.close()

# Initialize the database when the app starts
initialize_database()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/books', methods=['GET', 'POST'])
def books():
    conn = connect_db()
    cursor = conn.cursor()

    if request.method == 'POST':
        title = request.form['title']
        author_id = request.form['author_id']
        category_id = request.form['category_id']
        isbn = request.form['isbn']

        cursor.execute('INSERT INTO Books (Title, AuthorID, CategoryID, ISBN) VALUES (?, ?, ?, ?)',
                       (title, author_id, category_id, isbn))
        conn.commit()

    cursor.execute('SELECT * FROM Books')
    books = cursor.fetchall()
    conn.close()

    return render_template('books.html', books=books)

@app.route('/books/update/<int:book_id>', methods=['GET', 'POST'])
def update_book(book_id):
    conn = connect_db()
    cursor = conn.cursor()

    if request.method == 'POST':
        title = request.form['title']
        author_id = request.form['author_id']
        category_id = request.form['category_id']
        isbn = request.form['isbn']

        cursor.execute('''UPDATE Books SET Title = ?, AuthorID = ?, CategoryID = ?, ISBN = ? WHERE BookID = ?''',
                       (title, author_id, category_id, isbn, book_id))
        conn.commit()
        conn.close()
        return redirect(url_for('books'))

    cursor.execute('SELECT * FROM Books WHERE BookID = ?', (book_id,))
    book = cursor.fetchone()
    conn.close()
    return render_template('update_book.html', book=book)

@app.route('/books/delete/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Books WHERE BookID = ?', (book_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('books'))

@app.route('/members', methods=['GET', 'POST'])
def members():
    conn = connect_db()
    cursor = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        contact = request.form['contact']
        membership_date = request.form['membership_date']

        cursor.execute('INSERT INTO Members (Name, Contact, MembershipDate) VALUES (?, ?, ?)',
                       (name, contact, membership_date))
        conn.commit()

    cursor.execute('SELECT * FROM Members')
    members = cursor.fetchall()
    conn.close()

    return render_template('members.html', members=members)

@app.route('/members/update/<int:member_id>', methods=['GET', 'POST'])
def update_member(member_id):
    conn = connect_db()
    cursor = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        contact = request.form['contact']
        membership_date = request.form['membership_date']

        cursor.execute('''UPDATE Members SET Name = ?, Contact = ?, MembershipDate = ? WHERE MemberID = ?''',
                       (name, contact, membership_date, member_id))
        conn.commit()
        conn.close()
        return redirect(url_for('members'))

    cursor.execute('SELECT * FROM Members WHERE MemberID = ?', (member_id,))
    member = cursor.fetchone()
    conn.close()
    return render_template('update_member.html', member=member)

@app.route('/members/delete/<int:member_id>', methods=['POST'])
def delete_member(member_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Members WHERE MemberID = ?', (member_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('members'))

@app.route('/transactions', methods=['GET', 'POST'])
def transactions():
    conn = connect_db()
    cursor = conn.cursor()

    if request.method == 'POST':
        book_id = request.form['book_id']
        member_id = request.form['member_id']
        issue_date = request.form['issue_date']

        cursor.execute('INSERT INTO Transactions (BookID, MemberID, IssueDate) VALUES (?, ?, ?)',
                       (book_id, member_id, issue_date))
        conn.commit()

    cursor.execute('SELECT * FROM Transactions')
    transactions = cursor.fetchall()
    conn.close()

    return render_template('transactions.html', transactions=transactions)

@app.route('/transactions/update/<int:transaction_id>', methods=['GET', 'POST'])
def update_transaction(transaction_id):
    conn = connect_db()
    cursor = conn.cursor()

    if request.method == 'POST':
        return_date = request.form['return_date']

        cursor.execute('''UPDATE Transactions SET ReturnDate = ? WHERE TransactionID = ?''',
                       (return_date, transaction_id))
        conn.commit()
        conn.close()
        return redirect(url_for('transactions'))

    cursor.execute('SELECT * FROM Transactions WHERE TransactionID = ?', (transaction_id,))
    transaction = cursor.fetchone()
    conn.close()
    return render_template('update_transaction.html', transaction=transaction)

@app.route('/transactions/delete/<int:transaction_id>', methods=['POST'])
def delete_transaction(transaction_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Transactions WHERE TransactionID = ?', (transaction_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('transactions'))

if __name__ == '__main__':
    app.run(debug=True)
