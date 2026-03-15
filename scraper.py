
import requests
from bs4 import BeautifulSoup
import csv
import time
import re

CITIES = ["gdansk", "gdynia", "sopot"]
BASE_URL = "https://adresowo.pl/mieszkania/{city}/"
OUTPUT_CSV = "data/mieszkania_trojmiasto.csv"
PAGES_PER_CITY = 5
CSV_HEADERS = ["city", "title", "price", "area", "rooms", "link"]

def get_offer_links(soup):
    # Find all links to detailed offer pages
    links = set()
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if re.match(r"^/o/mieszkanie-", href):
            links.add("https://adresowo.pl" + href)
    return list(links)

def parse_offer_page(url):
    response = requests.get(url)
    if response.status_code != 200:
        return None
    soup = BeautifulSoup(response.text, "html.parser")
    # Title
    title_tag = soup.find("h1")
    title = title_tag.get_text(strip=True) if title_tag else ""
    # Price
    price = ""
    price_tag = soup.find(string=re.compile(r"zł"))
    if price_tag:
        price = price_tag.strip().replace("\xa0", " ")
    # Area and rooms
    area = ""
    rooms = ""
    details_text = soup.get_text(" ", strip=True)
    area_match = re.search(r"([0-9]+\.?[0-9]*) ?m²", details_text)
    rooms_match = re.search(r"([0-9]+) ?pok", details_text)
    if area_match:
        area = area_match.group(1)
    if rooms_match:
        rooms = rooms_match.group(1)
    return title, price, area, rooms

def scrape_city(city):
    listings_data = []
    for page in range(1, PAGES_PER_CITY + 1):
        url = BASE_URL.format(city=city)
        if page > 1:
            url += f"/?p={page}"
        print(f"Scraping {url}")
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to fetch {url}")
            continue
        soup = BeautifulSoup(response.text, "html.parser")
        offer_links = get_offer_links(soup)
        print(f"Found {len(offer_links)} offers on page {page}")
        for link in offer_links:
            try:
                title, price, area, rooms = parse_offer_page(link)
                listings_data.append([city, title, price, area, rooms, link])
                time.sleep(0.5)  # Be polite to the server
            except Exception as e:
                print(f"Error parsing {link}: {e}")
    return listings_data

def main():
    all_data = []
    for city in CITIES:
        city_data = scrape_city(city)
        all_data.extend(city_data)
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(CSV_HEADERS)
        writer.writerows(all_data)
    print(f"Saved {len(all_data)} listings to {OUTPUT_CSV}")

if __name__ == "__main__":
    main()
