"""
Item Catalog — Cross-domain items for recommendation
Derived from Yelp, Amazon Reviews, and Goodreads signals.
Domains: food, electronics, beauty, fashion, fintech, books, entertainment
"""

from typing import List, Dict, Any

# ── FOOD & SERVICES CATALOG (Yelp signals) ───────────────────────────────────
FOOD_ITEMS: List[Dict[str, Any]] = [
    {
        "id": "f001", "name": "Chicken Republic", "domain": "food",
        "category": "Fast Food Restaurant", "price_range": "budget",
        "tags": ["chicken", "jollof", "fast food", "nigerian", "quick"],
        "avg_rating": 4.1, "popularity": 0.90,
    },
    {
        "id": "f002", "name": "Buka Local Restaurant", "domain": "food",
        "category": "Local Nigerian Food", "price_range": "budget",
        "tags": ["amala", "ewedu", "pepper soup", "local", "nigerian", "traditional"],
        "avg_rating": 4.4, "popularity": 0.85,
    },
    {
        "id": "f003", "name": "Transcorp Hilton Restaurant", "domain": "food",
        "category": "Fine Dining", "price_range": "premium",
        "tags": ["fine dining", "continental", "premium", "abuja", "professional"],
        "avg_rating": 4.3, "popularity": 0.60,
    },
    {
        "id": "f004", "name": "Cold Stone Creamery", "domain": "food",
        "category": "Dessert", "price_range": "mid",
        "tags": ["ice cream", "dessert", "treat", "sweet", "fun"],
        "avg_rating": 4.2, "popularity": 0.75,
    },
    {
        "id": "f005", "name": "Suya Spot PH", "domain": "food",
        "category": "Street Food", "price_range": "budget",
        "tags": ["suya", "grilled meat", "street food", "spicy", "nigerian"],
        "avg_rating": 4.5, "popularity": 0.88,
    },
    {
        "id": "f006", "name": "Dominos Pizza Nigeria", "domain": "food",
        "category": "Pizza", "price_range": "mid",
        "tags": ["pizza", "western", "delivery", "fast food"],
        "avg_rating": 3.9, "popularity": 0.72,
    },
    {
        "id": "f007", "name": "Indomie Noodles", "domain": "food",
        "category": "Instant Food", "price_range": "budget",
        "tags": ["noodles", "cheap", "student", "instant", "affordable"],
        "avg_rating": 4.6, "popularity": 0.95,
    },
    {
        "id": "f008", "name": "Smokey Joes Bar and Grill", "domain": "food",
        "category": "Bar & Grill", "price_range": "mid",
        "tags": ["grilled", "bar", "social", "fun", "drinks", "nightlife"],
        "avg_rating": 4.1, "popularity": 0.70,
    },
    {
        "id": "f009", "name": "Chi Exotic Juice", "domain": "food",
        "category": "Beverages", "price_range": "budget",
        "tags": ["healthy", "juice", "family", "drinks", "natural"],
        "avg_rating": 4.0, "popularity": 0.80,
    },
    {
        "id": "f010", "name": "Kano Suya Spot", "domain": "food",
        "category": "Street Food", "price_range": "budget",
        "tags": ["suya", "northern", "nigerian", "spicy", "grilled"],
        "avg_rating": 4.6, "popularity": 0.87,
    },
]

# ── PRODUCTS CATALOG (Amazon signals) ────────────────────────────────────────
PRODUCT_ITEMS: List[Dict[str, Any]] = [
    {
        "id": "p001", "name": "Tecno Camon 30 Pro", "domain": "electronics",
        "category": "Smartphone", "price_range": "mid",
        "tags": ["phone", "camera", "android", "tech", "photography"],
        "avg_rating": 4.2, "popularity": 0.82,
    },
    {
        "id": "p002", "name": "Samsung Galaxy A54", "domain": "electronics",
        "category": "Smartphone", "price_range": "mid",
        "tags": ["phone", "samsung", "android", "reliable", "tech"],
        "avg_rating": 4.3, "popularity": 0.85,
    },
    {
        "id": "p003", "name": "JBL Portable Speaker", "domain": "electronics",
        "category": "Audio", "price_range": "mid",
        "tags": ["music", "speaker", "bluetooth", "portable", "fun"],
        "avg_rating": 4.4, "popularity": 0.78,
    },
    {
        "id": "p004", "name": "MAC Studio Fix Foundation", "domain": "beauty",
        "category": "Makeup", "price_range": "premium",
        "tags": ["makeup", "beauty", "foundation", "skin", "cosmetics"],
        "avg_rating": 4.5, "popularity": 0.80,
    },
    {
        "id": "p005", "name": "Nike Air Max Sneakers", "domain": "fashion",
        "category": "Footwear", "price_range": "premium",
        "tags": ["shoes", "fashion", "sport", "lifestyle", "brand"],
        "avg_rating": 4.4, "popularity": 0.87,
    },
    {
        "id": "p006", "name": "Ankara Print Dress", "domain": "fashion",
        "category": "Clothing", "price_range": "budget",
        "tags": ["fashion", "nigerian", "ankara", "cultural", "style"],
        "avg_rating": 4.6, "popularity": 0.83,
    },
    {
        "id": "p007", "name": "Opay POS Machine", "domain": "fintech",
        "category": "Business Tool", "price_range": "mid",
        "tags": ["business", "fintech", "pos", "payments", "entrepreneur"],
        "avg_rating": 4.3, "popularity": 0.75,
    },
    {
        "id": "p008", "name": "Cowrywise Investment App", "domain": "fintech",
        "category": "Financial App", "price_range": "free",
        "tags": ["savings", "investment", "fintech", "money", "wealth"],
        "avg_rating": 4.2, "popularity": 0.72,
    },
    {
        "id": "p009", "name": "Konga Grocery Delivery", "domain": "products",
        "category": "Grocery", "price_range": "budget",
        "tags": ["grocery", "delivery", "family", "affordable", "convenience"],
        "avg_rating": 3.8, "popularity": 0.70,
    },
    {
        "id": "p010", "name": "Amazon Kindle Paperwhite", "domain": "electronics",
        "category": "E-Reader", "price_range": "mid",
        "tags": ["books", "reading", "tech", "education", "premium"],
        "avg_rating": 4.6, "popularity": 0.74,
    },
]

# ── BOOKS CATALOG (Goodreads signals) ────────────────────────────────────────
BOOK_ITEMS: List[Dict[str, Any]] = [
    {
        "id": "b001", "name": "Things Fall Apart — Chinua Achebe", "domain": "books",
        "category": "African Literature", "price_range": "budget",
        "tags": ["african", "classic", "culture", "nigeria", "literature", "identity"],
        "avg_rating": 4.7, "popularity": 0.92,
    },
    {
        "id": "b002", "name": "Atomic Habits — James Clear", "domain": "books",
        "category": "Self Development", "price_range": "budget",
        "tags": ["self help", "habits", "productivity", "growth", "motivation"],
        "avg_rating": 4.8, "popularity": 0.95,
    },
    {
        "id": "b003", "name": "Purple Hibiscus — Chimamanda Adichie", "domain": "books",
        "category": "African Fiction", "price_range": "budget",
        "tags": ["african", "nigerian", "fiction", "family", "culture", "female"],
        "avg_rating": 4.5, "popularity": 0.85,
    },
    {
        "id": "b004", "name": "Rich Dad Poor Dad — Robert Kiyosaki", "domain": "books",
        "category": "Finance", "price_range": "budget",
        "tags": ["finance", "money", "investment", "business", "wealth", "entrepreneur"],
        "avg_rating": 4.3, "popularity": 0.90,
    },
    {
        "id": "b005", "name": "The Alchemist — Paulo Coelho", "domain": "books",
        "category": "Fiction", "price_range": "budget",
        "tags": ["fiction", "inspirational", "journey", "philosophy", "motivation"],
        "avg_rating": 4.6, "popularity": 0.93,
    },
    {
        "id": "b006", "name": "How to Win Friends — Dale Carnegie", "domain": "books",
        "category": "Self Development", "price_range": "budget",
        "tags": ["social", "communication", "business", "relationships", "professional"],
        "avg_rating": 4.4, "popularity": 0.88,
    },
    {
        "id": "b007", "name": "Medical Biochemistry — Baynes", "domain": "books",
        "category": "Medical Textbook", "price_range": "premium",
        "tags": ["medical", "science", "textbook", "professional", "health"],
        "avg_rating": 4.2, "popularity": 0.55,
    },
    {
        "id": "b008", "name": "Zero to One — Peter Thiel", "domain": "books",
        "category": "Business", "price_range": "budget",
        "tags": ["startup", "business", "innovation", "entrepreneurship", "tech"],
        "avg_rating": 4.4, "popularity": 0.85,
    },
    {
        "id": "b009", "name": "Udemy Online Course (Tech)", "domain": "education",
        "category": "Online Learning", "price_range": "budget",
        "tags": ["education", "learning", "tech", "skills", "career", "online"],
        "avg_rating": 4.3, "popularity": 0.80,
    },
]

# ── ENTERTAINMENT CATALOG ─────────────────────────────────────────────────────
ENTERTAINMENT_ITEMS: List[Dict[str, Any]] = [
    {
        "id": "e001", "name": "Netflix Nigeria Subscription", "domain": "entertainment",
        "category": "Streaming", "price_range": "mid",
        "tags": ["movies", "nollywood", "streaming", "series", "binge"],
        "avg_rating": 4.0, "popularity": 0.88,
    },
    {
        "id": "e002", "name": "PUBG Mobile", "domain": "entertainment",
        "category": "Mobile Game", "price_range": "free",
        "tags": ["gaming", "mobile", "battle royale", "online", "fun", "student"],
        "avg_rating": 4.3, "popularity": 0.85,
    },
    {
        "id": "e003", "name": "Audiomack Music App", "domain": "entertainment",
        "category": "Music", "price_range": "free",
        "tags": ["music", "afrobeats", "nigerian", "streaming", "free"],
        "avg_rating": 4.4, "popularity": 0.90,
    },
    {
        "id": "e004", "name": "DSTV Premium Package", "domain": "entertainment",
        "category": "Cable TV", "price_range": "premium",
        "tags": ["tv", "sports", "movies", "news", "cable", "football"],
        "avg_rating": 3.8, "popularity": 0.75,
    },
    {
        "id": "e005", "name": "Showmax Nigeria", "domain": "entertainment",
        "category": "Streaming", "price_range": "budget",
        "tags": ["movies", "nollywood", "streaming", "local", "affordable"],
        "avg_rating": 4.0, "popularity": 0.72,
    },
]

# ── COMBINED CATALOG ──────────────────────────────────────────────────────────
ALL_ITEMS: List[Dict[str, Any]] = (
    FOOD_ITEMS + PRODUCT_ITEMS + BOOK_ITEMS + ENTERTAINMENT_ITEMS
)

ITEM_LOOKUP: Dict[str, Dict[str, Any]] = {
    item["id"]: item for item in ALL_ITEMS
}

# ── Catalog stats (for API response) ─────────────────────────────────────────
CATALOG_STATS = {
    "total": len(ALL_ITEMS),
    "food": len(FOOD_ITEMS),
    "products": len(PRODUCT_ITEMS),
    "books": len(BOOK_ITEMS),
    "entertainment": len(ENTERTAINMENT_ITEMS),
    "domains": sorted(set(i["domain"] for i in ALL_ITEMS)),
}
