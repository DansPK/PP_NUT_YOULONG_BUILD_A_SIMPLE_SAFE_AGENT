import sqlite3


from db.db import DB_PATH

def search_books(title: str) -> list[dict]:
    with sqlite3.connect(DB_PATH) as connection:
        connection.row_factory = sqlite3.Row
        rows = connection.execute(
            """
            SELECT id, title, author
            FROM books
            WHERE title LIKE ?
            """,
            (f"%{title}%",),
        ).fetchall()

    return [dict(row) for row in rows]

def check_availability(book_id: int) -> dict | None:
    with sqlite3.connect(DB_PATH) as connection:
        connection.row_factory = sqlite3.Row
        row = connection.execute(
            """
            SELECT id, title, available_copies
            FROM books
            WHERE id = ?
            """,
            (book_id,),
        ).fetchone()

    return dict(row) if row else None

def borrow_book(book_id: int) -> bool:
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.execute(
            """
            UPDATE books
            SET available_copies = available_copies - 1
            WHERE id = ? AND available_copies > 0
            """,
            (book_id,),
        )
        return cursor.rowcount == 1

def list_books() -> list[dict]:
    with sqlite3.connect(DB_PATH) as connection:
        connection.row_factory = sqlite3.Row
        rows = connection.execute(
            "SELECT id, title, author FROM books ORDER BY id"
        ).fetchall()

    return [dict(row) for row in rows]

def create_book(title: str, author: str, available_copies: int) -> dict :
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.execute(
            """
            INSERT INTO books (title, author, available_copies)
            values (?,?,?)
            """,
            (title, author, available_copies),
        )
        return {
            "id": cursor.lastrowid,
            "title": title,
            "author": author,
            "available_copies": available_copies,
        }

def update_book(book_id: int, title: str, author: str, available_copies: int) -> dict | None:
    with sqlite3.connect(DB_PATH) as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.execute(
            """
            UPDATE books
            SET title = ?, author = ?, available_copies = ?
            WHERE id = ?
            """,
            (title, author, available_copies, book_id),
        )
        if cursor.rowcount == 0:
            return None

        row = connection.execute(
            """
            SELECT id, title, author, available_copies
            FROM books
            WHERE id = ?
            """,
            (book_id,),
        ).fetchone()

        return dict(row)

def delete_book(book_id: int) -> dict | None:
    with sqlite3.connect(DB_PATH) as connection:
        connection.row_factory = sqlite3.Row

        row = connection.execute(
            """
            SELECT id, title, author, available_copies
            FROM books
            WHERE id = ?
            """,
            (book_id,),
        ).fetchone()

        if row is None:
            return None

        connection.execute(
            "DELETE FROM books WHERE id = ?",
            (book_id,),
        )
        return dict(row)
