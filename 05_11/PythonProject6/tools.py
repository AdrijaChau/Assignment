import json
from pathlib import Path
from langchain.tools import tool

FILE = Path(__file__).parent / "workshops.json"
COUPONS_FILE = Path(__file__).parent / "coupons.json"


def get_workshops():
    return json.loads(FILE.read_text(encoding="utf-8"))


def get_coupons():
    if COUPONS_FILE.exists():
        return json.loads(COUPONS_FILE.read_text(encoding="utf-8"))
    return []


@tool
def search_workshops(keyword: str) -> str:
    """Search available workshops by title."""
    matches = [
        w for w in get_workshops()
        if keyword.lower() in w["title"].lower()
    ]
    return json.dumps(matches)


@tool
def list_all_workshops() -> str:
    """List all available workshops."""
    return json.dumps(get_workshops())


@tool
def find_cheapest_workshop() -> str:
    """Find the workshop with the lowest fee."""
    workshops = get_workshops()
    if not workshops:
        return "No workshops available."
    cheapest = min(workshops, key=lambda x: x["fee"])
    return json.dumps(cheapest)


@tool
def calculate_workshop_fee(workshop_id: str, participants: int, coupon_code: str = "") -> str:
    """Calculate the total fee for a workshop and participant count, optionally applying a coupon code."""
    if participants < 1 or participants > 30:
        return "Participant count must be between 1 and 30."

    workshops = get_workshops()
    selected_workshop = None
    for workshop in workshops:
        if workshop["id"] == workshop_id:
            selected_workshop = workshop
            break

    if not selected_workshop:
        return "Workshop not found."

    total = selected_workshop["fee"] * participants
    discount_applied = 0

    if coupon_code:
        coupons = get_coupons()
        valid_coupon = next((c for c in coupons if c["code"].upper() == coupon_code.upper()), None)
        if valid_coupon:
            discount_percentage = valid_coupon["discount_percentage"]
            discount_applied = (total * discount_percentage) / 100
            total -= discount_applied
        else:
            return json.dumps({
                "error": "Invalid coupon code",
                "workshop": selected_workshop["title"],
                "participants": participants,
                "total_fee": total
            })

    return json.dumps({
        "workshop": selected_workshop["title"],
        "participants": participants,
        "original_fee": selected_workshop["fee"] * participants,
        "discount_applied": discount_applied,
        "total_fee": total
    })


