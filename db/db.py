"""Create the small SQLite database used by the library agent."""

import sqlite3
from pathlib import Path


DB_PATH = Path(__file__).with_name("library.db")


def init_db(db_path: Path = DB_PATH) -> None:
    with sqlite3.connect(db_path) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                available_copies INTEGER NOT NULL CHECK (available_copies >= 0)
            )
            """
        )
        connection.executemany(
            """
            INSERT OR IGNORE INTO books (id, title, author, available_copies)
            VALUES (?, ?, ?, ?)
            """,
            [
                (1, "The Hobbit", "J. R. R. Tolkien", 3),
                (2, "1984", "George Orwell", 2),
                (3, "Pride and Prejudice", "Jane Austen", 0),
            ],
        )


if __name__ == "__main__":
    init_db()
    print(f"Library database ready: {DB_PATH}")
