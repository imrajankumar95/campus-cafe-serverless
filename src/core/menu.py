"""Fixed café menu. Must match the item IDs in frontend/menu.js."""

# Prices in cents (whole numbers) to avoid float rounding errors like 0.1 + 0.2.
MENU = {
    # Hot coffee
    "espresso": {"name": "Espresso", "price_cents": 295},
    "americano": {"name": "Americano", "price_cents": 325},
    "latte": {"name": "Latte", "price_cents": 445},
    "cappuccino": {"name": "Cappuccino", "price_cents": 445},
    "mocha": {"name": "Mocha", "price_cents": 495},
    # Cold drinks
    "cold-brew": {"name": "Cold Brew", "price_cents": 425},
    "iced-latte": {"name": "Iced Latte", "price_cents": 475},
    "iced-caramel": {"name": "Iced Caramel Macchiato", "price_cents": 545},
    "iced-americano": {"name": "Iced Americano", "price_cents": 375},
    "matcha-latte": {"name": "Matcha Iced Latte", "price_cents": 525},
    # Food
    "croissant": {"name": "Butter Croissant", "price_cents": 325},
    "muffin": {"name": "Blueberry Muffin", "price_cents": 325},
    "bagel": {"name": "Bagel + Cream Cheese", "price_cents": 375},
    "chicken-sandwich": {"name": "Chicken Sandwich", "price_cents": 845},
    "avocado-toast": {"name": "Avocado Toast", "price_cents": 895},
}


def is_on_menu(item_id: str) -> bool:
    return item_id in MENU


def price_cents(item_id: str) -> int:
    return MENU[item_id]["price_cents"]