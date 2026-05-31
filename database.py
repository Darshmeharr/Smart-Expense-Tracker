import sqlite3

DB_NAME = "expenses.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        category TEXT,
        description TEXT,
        amount REAL,
        type TEXT
    )
    """)

    conn.commit()
    conn.close()


def insert_transaction(date, category, description, amount, transaction_type):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO transactions
    (date, category, description, amount, type)
    VALUES (?, ?, ?, ?, ?)
    """, (date, category, description, amount, transaction_type))

    conn.commit()
    conn.close()


def fetch_transactions():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM transactions
    ORDER BY date DESC
    """)

    data = cursor.fetchall()

    conn.close()
    return data


def delete_transaction(transaction_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM transactions
    WHERE id = ?
    """, (transaction_id,))

    conn.commit()
    conn.close()
