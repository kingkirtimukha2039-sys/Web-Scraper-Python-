# ============================================
# WEB SCRAPER - Python Project
# By: [Your Name] | Portfolio Project
# ============================================
# SETUP: pip install requests beautifulsoup4
# Run:   python web_scraper.py
# ============================================

import requests
from bs4 import BeautifulSoup
import csv
import json
from datetime import datetime

# ── HEADERS (makes requests look like a browser) ──
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}


# ── 1. SCRAPE QUOTES ────────────────────────────
def scrape_quotes():
    """Scrape quotes from quotes.toscrape.com (a safe practice site)."""
    print("\n🔍 Scraping quotes from quotes.toscrape.com ...")
    url    = "http://quotes.toscrape.com"
    quotes = []

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        soup     = BeautifulSoup(response.text, "html.parser")
        items    = soup.find_all("div", class_="quote")

        for item in items:
            text   = item.find("span", class_="text").get_text(strip=True)
            author = item.find("small", class_="author").get_text(strip=True)
            tags   = [t.get_text(strip=True) for t in item.find_all("a", class_="tag")]
            quotes.append({"quote": text, "author": author, "tags": tags})

        print(f"✅ Found {len(quotes)} quotes!\n")
        for i, q in enumerate(quotes, 1):
            print(f"{i}. {q['quote'][:60]}...")
            print(f"   — {q['author']} | Tags: {', '.join(q['tags'])}\n")

        return quotes

    except Exception as e:
        print(f"❌ Error: {e}")
        return []


# ── 2. SCRAPE BOOK TITLES & PRICES ──────────────
def scrape_books():
    """Scrape books from books.toscrape.com (a safe practice site)."""
    print("\n📚 Scraping books from books.toscrape.com ...")
    url   = "http://books.toscrape.com"
    books = []

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        soup     = BeautifulSoup(response.text, "html.parser")
        items    = soup.find_all("article", class_="product_pod")

        for item in items:
            title  = item.find("h3").find("a")["title"]
            price  = item.find("p", class_="price_color").get_text(strip=True)
            rating = item.find("p", class_="star-rating")["class"][1]
            books.append({"title": title, "price": price, "rating": rating})

        print(f"✅ Found {len(books)} books!\n")
        for i, b in enumerate(books[:5], 1):   # show first 5
            print(f"{i}. {b['title'][:50]}")
            print(f"   Price: {b['price']} | Rating: {b['rating']}\n")

        return books

    except Exception as e:
        print(f"❌ Error: {e}")
        return []


# ── 3. SAVE TO CSV ───────────────────────────────
def save_to_csv(data, filename):
    """Save scraped data to a CSV file."""
    if not data:
        print("❌ No data to save.")
        return

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

    print(f"💾 Data saved to {filename}")


# ── 4. SAVE TO JSON ──────────────────────────────
def save_to_json(data, filename):
    """Save scraped data to a JSON file."""
    if not data:
        print("❌ No data to save.")
        return

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"💾 Data saved to {filename}")


# ── MAIN MENU ────────────────────────────────────
def main():
    print("=" * 45)
    print("         WEB SCRAPER - Python")
    print("=" * 45)
    print("1. Scrape Quotes")
    print("2. Scrape Books (title + price)")
    print("3. Scrape Quotes & Save to CSV")
    print("4. Scrape Books & Save to JSON")
    print("5. Exit")
    print("=" * 45)

    choice = input("Enter choice (1-5): ").strip()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    if choice == "1":
        scrape_quotes()

    elif choice == "2":
        scrape_books()

    elif choice == "3":
        data = scrape_quotes()
        if data:
            save_to_csv(data, f"quotes_{timestamp}.csv")

    elif choice == "4":
        data = scrape_books()
        if data:
            save_to_json(data, f"books_{timestamp}.json")

    elif choice == "5":
        print("👋 Goodbye!")

    else:
        print("❌ Invalid choice. Please enter 1–5.")


if __name__ == "__main__":
    main()


# ============================================
# HOW TO USE:
# 1. pip install requests beautifulsoup4
# 2. Run: python web_scraper.py
# 3. Choose what to scrape
# 4. Data saves as CSV or JSON file
# ============================================
