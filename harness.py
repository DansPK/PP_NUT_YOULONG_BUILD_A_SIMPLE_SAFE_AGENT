import sqlite3

from tools import TOOL_REGISTRY


TOOL_PERMISSIONS = {
    "list_books": {"visitor", "member", "admin"},
    "search_books": {"visitor", "member", "admin"},
    "check_availability": {"visitor", "member", "admin"},
    "borrow_book": {"member", "admin"},
    "create_book": {"admin"},
    "update_book": {"admin"},
    "delete_book": {"admin"},
}


def run_tool(name: str, args: dict, role: str, confirm_delete=None) -> dict:
    if name not in TOOL_REGISTRY or not isinstance(args, dict):
        return {"error": "Invalid tool call"}

    if role not in TOOL_PERMISSIONS.get(name, set()):
        return {"error": "Permission denied"}

    if name == "list_books":
        if args:
            return {"error": "list_books takes no arguments"}
        values = ()

    elif name == "search_books":
        title = args.get("title")
        if not isinstance(title, str) or not title.strip():
            return {"error": "Invalid title"}
        values = (title.strip(),)

    elif name == "create_book":
        title = args.get("title")
        author = args.get("author")
        copies = args.get("available_copies")

        if not isinstance(title, str) or not title.strip():
            return {"error": "Invalid title"}
        if not isinstance(author, str) or not author.strip():
            return {"error": "Invalid author"}
        if type(copies) is not int or copies < 0:
            return {"error": "Invalid available copies"}

        values = (title.strip(), author.strip(), copies)
    elif name == "update_book":
        book_id = args.get("book_id")
        title = args.get("title")
        author = args.get("author")
        copies = args.get("available_copies")

        if type(book_id) is not int or book_id <= 0:
            return {"error": "Invalid book ID"}
        if not isinstance(title, str) or not title.strip():
            return {"error": "Invalid title"}
        if not isinstance(author, str) or not author.strip():
            return {"error": "Invalid author"}
        if type(copies) is not int or copies < 0:
            return {"error": "Invalid available copies"}

        values = (book_id, title.strip(), author.strip(), copies)

    else:
        book_id = args.get("book_id")
        if type(book_id) is not int or book_id <= 0:
            return {"error": "Invalid book ID"}
        values = (book_id,)

    try:
        if name == "delete_book":
            book = TOOL_REGISTRY["check_availability"](book_id)
            if book is None:
                return {"error": "Book not found"}
            if confirm_delete is None or not confirm_delete(book):
                return {"error": "Deletion cancelled"}

        return {"result": TOOL_REGISTRY[name](*values)}
    except sqlite3.Error:
        return {"error": "Database operation failed"}
