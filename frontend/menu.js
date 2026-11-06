// Fixed menu. The API validates orders against the same item IDs,
// so keep this list in sync with the backend.
window.CAFE_CATEGORIES = [
  { id: "hot",  name: "Hot drinks",  emoji: "☕", blurb: "Espresso classics, tea and cocoa." },
  { id: "cold", name: "Cold drinks", emoji: "🧊", blurb: "Iced coffee, lemonade and smoothies." },
  { id: "food", name: "Food",        emoji: "🥐", blurb: "Fresh bakes, sandwiches and salads." }
];

window.CAFE_MENU = [
  { id: "espresso",      category: "hot",  emoji: "☕", name: "Espresso",          description: "Double shot, rich and short.",      price: 2.75 },
  { id: "latte",         category: "hot",  emoji: "🥛", name: "Latte",             description: "Espresso with steamed milk.",       price: 4.25 },
  { id: "cappuccino",    category: "hot",  emoji: "☕", name: "Cappuccino",        description: "Equal parts espresso, milk, foam.", price: 4.25 },
  { id: "tea",           category: "hot",  emoji: "🍵", name: "Tea",               description: "Black, green or herbal.",           price: 2.25 },
  { id: "hot-chocolate", category: "hot",  emoji: "🍫", name: "Hot chocolate",     description: "Made with real cocoa.",             price: 3.50 },

  { id: "iced-coffee",   category: "cold", emoji: "🧊", name: "Iced coffee",       description: "Cold-brewed, served over ice.",     price: 3.75 },
  { id: "iced-latte",    category: "cold", emoji: "🥤", name: "Iced latte",        description: "Espresso and cold milk.",           price: 4.75 },
  { id: "lemonade",      category: "cold", emoji: "🍋", name: "Lemonade",          description: "Fresh-squeezed, lightly sweet.",    price: 3.25 },
  { id: "smoothie",      category: "cold", emoji: "🍓", name: "Berry smoothie",    description: "Mixed berries, banana, yogurt.",    price: 5.50 },

  { id: "croissant",     category: "food", emoji: "🥐", name: "Butter croissant",  description: "Baked fresh every morning.",        price: 3.25 },
  { id: "muffin",        category: "food", emoji: "🧁", name: "Blueberry muffin",  description: "Soft, with a crumb top.",           price: 2.95 },
  { id: "bagel",         category: "food", emoji: "🥯", name: "Bagel",             description: "With cream cheese.",                price: 3.50 },
  { id: "sandwich",      category: "food", emoji: "🥪", name: "Chicken sandwich",  description: "Grilled chicken, greens, aioli.",   price: 7.50 },
  { id: "salad",         category: "food", emoji: "🥗", name: "Garden salad bowl", description: "Seasonal greens, vinaigrette.",     price: 8.95 }
];
