import json
import os

BOOKS_FILE = "books.json"
RESERVATIONS_FILE = "reservations.json"


def load_json(filepath):
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(filepath, data):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def search_books(query: str) -> str:
    """
    Search for books by splitting the query into keywords and matching any.
    """
    books = load_json(BOOKS_FILE)
    keywords = query.lower().split()

    results = []
    for book in books:
        book_text = f"{book['title']} {book['author']} {book['category']}".lower()
        # If any keyword matches the book details, include it
        if any(kw in book_text for kw in keywords):
            results.append(book)

    if not results:
        return json.dumps({"message": f"No books found matching '{query}'."})

    return json.dumps(results, indent=2)

def reserve_book(book_id: int, customer_name: str) -> str:
    """
    Reserve a book using its Book ID and the customer's name.
    Checks availability before confirming reservation.
    """
    books = load_json(BOOKS_FILE)
    reservations = load_json(RESERVATIONS_FILE)

    # Locate book by ID
    target_book = None
    for book in books:
        if book["id"] == int(book_id):
            target_book = book
            break

    if not target_book:
        return json.dumps({"error": f"Book with ID {book_id} not found."})

    if target_book["available_copies"] <= 0:
        return json.dumps(
            {"error": f"Sorry, '{target_book['title']}' is currently out of stock and cannot be reserved."})

    # Deduct available copy count
    target_book["available_copies"] -= 1
    save_json(BOOKS_FILE, books)

    # Create reservation record
    reservation = {
        "reservation_id": len(reservations) + 1,
        "book_id": target_book["id"],
        "book_title": target_book["title"],
        "customer_name": customer_name,
        "status": "Confirmed"
    }
    reservations.append(reservation)
    save_json(RESERVATIONS_FILE, reservations)

    return json.dumps({"success": True, "reservation": reservation}, indent=2)