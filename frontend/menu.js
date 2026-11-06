// Fixed menu. The API validates orders against the same item IDs,
// so keep this list in sync with the backend.
// Icons are Lucide names: https://lucide.dev/icons
window.CAFE_CATEGORIES = [
  { id: "hot",  name: "Hot coffee",  icon: "coffee",   blurb: "Espresso classics, pulled fresh to order." },
  { id: "cold", name: "Cold drinks", icon: "cup-soda", blurb: "Cold brew, iced lattes and matcha." },
  { id: "food", name: "Food",        icon: "croissant", blurb: "Fresh bakes, sandwiches and toast." }
];

window.CAFE_MENU = [
  { id: "espresso",        category: "hot",  icon: "coffee",     name: "Espresso",               description: "Double shot, bold and smooth.",              price: 2.95 },
  { id: "americano",       category: "hot",  icon: "coffee",     name: "Americano",              description: "Espresso topped with hot water.",            price: 3.25 },
  { id: "latte",           category: "hot",  icon: "milk",       name: "Latte",                  description: "Espresso with silky steamed milk.",          price: 4.45, popular: true },
  { id: "cappuccino",      category: "hot",  icon: "coffee",     name: "Cappuccino",             description: "Espresso, steamed milk, thick foam.",        price: 4.45 },
  { id: "mocha",           category: "hot",  icon: "cookie",     name: "Mocha",                  description: "Espresso, chocolate and steamed milk.",      price: 4.95 },

  { id: "cold-brew",       category: "cold", icon: "cup-soda",   name: "Cold Brew",              description: "Steeped 18 hours, smooth and strong.",       price: 4.25, popular: true },
  { id: "iced-latte",      category: "cold", icon: "glass-water", name: "Iced Latte",            description: "Espresso and cold milk over ice.",           price: 4.75 },
  { id: "iced-caramel",    category: "cold", icon: "cup-soda",   name: "Iced Caramel Macchiato", description: "Vanilla, milk, espresso and caramel drizzle.", price: 5.45 },
  { id: "iced-americano",  category: "cold", icon: "glass-water", name: "Iced Americano",        description: "Espresso and cold water over ice.",          price: 3.75 },
  { id: "matcha-latte",    category: "cold", icon: "leaf",       name: "Matcha Iced Latte",      description: "Ceremonial matcha with cold milk.",          price: 5.25 },

  { id: "croissant",       category: "food", icon: "croissant",  name: "Butter Croissant",       description: "Flaky, baked fresh every morning.",          price: 3.25 },
  { id: "muffin",          category: "food", icon: "cake-slice", name: "Blueberry Muffin",       description: "Soft, with a crumb top.",                    price: 3.25 },
  { id: "bagel",           category: "food", icon: "donut",      name: "Bagel + Cream Cheese",   description: "Toasted sesame bagel.",                      price: 3.75 },
  { id: "chicken-sandwich", category: "food", icon: "sandwich",  name: "Chicken Sandwich",       description: "Grilled chicken, greens, garlic aioli.",     price: 8.45, popular: true },
  { id: "avocado-toast",   category: "food", icon: "wheat",      name: "Avocado Toast",          description: "Sourdough, smashed avocado, chili flakes.",  price: 8.95 }
];
