TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_books",
            "description": "Find books by part of their title.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "minLength": 1}
                },
                "required": ["title"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "check_availability",
            "description": "Check available copies of a book by its ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "book_id": {"type": "integer", "minimum": 1}
                },
                "required": ["book_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "borrow_book",
            "description": "Borrow one available copy of a book by its ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "book_id": {"type": "integer", "minimum": 1}
                },
                "required": ["book_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_books",
            "description": "List every book in the library catalog.",
            "parameters": {
                "type": "object",
                "properties": {},
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "create_book",
            "description": "Add a new book to the library catalog.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "minLength": 1},
                    "author": {"type": "string", "minLength": 1},
                    "available_copies": {"type": "integer", "minimum": 0},
                },
                "required": ["title", "author", "available_copies"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "update_book",
            "description": "Update an existing book's title, author, and available copies.",
            "parameters": {
                "type": "object",
                "properties": {
                    "book_id": {"type": "integer", "minimum": 1},
                    "title": {"type": "string", "minLength": 1},
                    "author": {"type": "string", "minLength": 1},
                    "available_copies": {"type": "integer", "minimum": 0},
                },
                "required": ["book_id", "title", "author", "available_copies"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "delete_book",
            "description": "Delete a book by ID after the admin confirms it.",
            "parameters": {
                "type": "object",
                "properties": {
                    "book_id": {"type": "integer", "minimum": 1},
                },
                "required": ["book_id"],
            },
        },
    },

]
