import json

from pathlib import Path

from langchain.tools import tool

# Get the JSON file location

BASE_DIR = Path(__file__).resolve().parent

RESTAURANT_FILE = BASE_DIR / "restaurants.json"


# Load restaurant data

def get_restaurants():
    with open(RESTAURANT_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


# TOOL 1: Search restaurants

@tool
def search_restaurants(keyword: str) -> str:
    """

    Search restaurants using cuisine type or restaurant name.

    Display matching restaurants with prices and available seats.

    """

    restaurants = get_restaurants()

    keyword = keyword.lower()

    matches = []

    for restaurant in restaurants:

        if (

                keyword in restaurant["cuisine"].lower()

                or keyword in restaurant["name"].lower()

                or keyword in restaurant["location"].lower()

        ):
            matches.append(restaurant)

    if not matches:
        return "No matching restaurants found."

    return json.dumps(matches, indent=4)


# TOOL 2: Calculate dining cost

@tool
def calculate_dining_cost(

        restaurant_id: str,

        guests: int

) -> str:
    """

    Calculate estimated dining cost using restaurant ID and guest count.

    """

    # Validate guest count

    if guests < 1 or guests > 20:
        return "Guest count must be between 1 and 20."

    restaurants = get_restaurants()

    # Find restaurant

    for restaurant in restaurants:

        if restaurant["id"].upper() == restaurant_id.upper():
            price = restaurant["price_per_person"]

            total_cost = price * guests

            result = {

                "restaurant": restaurant["name"],

                "restaurant_id": restaurant_id,

                "guests": guests,

                "price_per_person": price,

                "total_estimated_cost": total_cost,

                "available_seats": restaurant["available_seats"]

            }

            return json.dumps(result, indent=4)

    return "Restaurant not found."


# TESTING BOTH TOOLS

if __name__ == "__main__":
    print("\n===== SEARCH RESTAURANTS =====")

    print(

        search_restaurants.invoke({

            "keyword": "Indian"

        })

    )

    print("\n===== CALCULATE DINING COST =====")

    print(

        calculate_dining_cost.invoke({

            "restaurant_id": "R101",

            "guests": 4

        })

    )

import re


# STEP 1: Detect PII in user input

def contains_pii(text):
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'

    phone_pattern = r'(?<!\w)(?:\+?\d[\d\s().-]{7,}\d)(?!\w)'

    if re.search(email_pattern, text):
        return True

    if re.search(phone_pattern, text):
        return True

    return False


# STEP 2: Clean AI output

def clean_output(text):
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'

    phone_pattern = r'(?<!\w)(?:\+?\d[\d\s().-]{7,}\d)(?!\w)'

    text = re.sub(email_pattern, "[EMAIL REDACTED]", text)

    text = re.sub(phone_pattern, "[PHONE REDACTED]", text)

    return text


# STEP 3: Validate guest count

def validate_guest_count(guests):
    if guests < 1 or guests > 20:
        return False

    return True


# STEP 4: Domain restriction

def is_restaurant_question(question):
    keywords = [

        "restaurant",

        "food",

        "cuisine",

        "dining",

        "dinner",

        "lunch",

        "breakfast",

        "price",

        "cost",

        "guest",

        "people",

        "seat",

        "indian",

        "italian",

        "chinese",

        "booking",

        "reservation",

        "menu",

        "spice garden"

    ]

    question = question.lower()

    return any(word in question for word in keywords)



