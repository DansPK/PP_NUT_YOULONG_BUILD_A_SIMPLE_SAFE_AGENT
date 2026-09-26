from infra.sqlite_tools import (
    search_books,
    check_availability,
    borrow_book,
    list_books,
    create_book,
    update_book,
    delete_book,
)

TOOL_REGISTRY = {
    "search_books": search_books,
    "check_availability": check_availability,
    "borrow_book": borrow_book,
    "list_books": list_books,
    "create_book": create_book,
    "update_book": update_book,
    "delete_book": delete_book,
}
