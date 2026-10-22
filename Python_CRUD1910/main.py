from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2

app = FastAPI()


def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="library_store",
        user="postgres",
        password="Admin@123",
    )

conn = get_connection()
cur = conn.cursor()

# query = """
# INSERT INTO books
# (book_id, title, author, category, price, stock)
# VALUES
# (%s, %s, %s, %s, %s, %s)
# """
#
# books = [
#     (201, 'Atomic Habits', 'James Clear', 'Self Help', 650, 12),
#     (202, 'Clean Code', 'Robert Martin', 'Technology', 900, 8),
#     (203, 'The Alchemist', 'Paulo Coelho', 'Fiction', 500, 15),
#     (204, 'Deep Work', 'Cal Newport', 'Productivity', 700, 10)
# ]
#
# cur.executemany(query, books)
#
# conn.commit()
#
# print("4 books inserted successfully.")
#
# cur.close()
# conn.close()

@app.get("/books")
def get_books():
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM books")
        books = cur.fetchall()
        return books
    finally:
        cur.close()
        conn.close()


@app.get("/book")
def get_books():
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM books WHERE price >600")
        books = cur.fetchall()
        return books
    finally:
        cur.close()
        conn.close()
