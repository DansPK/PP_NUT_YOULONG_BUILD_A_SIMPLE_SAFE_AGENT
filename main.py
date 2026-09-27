from agent import run_agents



# Human approval for deleting books
def confirm_delete(book: dict) -> bool:
    answer = input(
        f"Delete book #{book['id']} — {book['title']}? (yes/no): "
    )
    return answer.strip().lower() == "yes"

def main():
    role = input("Role (visitor/member/admin): ").strip().lower()
    if role not in {"visitor", "member", "admin"}:
        print("Invalid role.")
        return

    history = []
    print("Library chat started. Type 'quit' to exit.")

    while True:
        request = input("\nYou: ").strip()

        if request.lower() == "quit":
            break
        if not request:
            continue

        answer, history = run_agents(request, role, history, confirm_delete, debug=True)
        print("Agent:", answer)


if __name__ == "__main__":
    main()
