import requests
from bs4 import BeautifulSoup
import json
import logging
from db.db_connection import get_connection
from datetime import datetime
import os

# Logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(filename="logs/scraper.log", level=logging.INFO)

def scrape_example():
    url = "https://example.com"
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        title = soup.title.string if soup.title else "Sin título"
        content = soup.get_text()

        # Persistencia
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO scraped_data (title, url, content) VALUES (%s, %s, %s)", (title, url, content))
        conn.commit()
        cur.close()
        conn.close()

        # JSON export
        os.makedirs("data", exist_ok=True)
        with open("data/sample_export.json", "w", encoding="utf-8") as f:
            json.dump({
                "title": title,
                "url": url,
                "content": content[:300] + "...",
                "scraped_at": str(datetime.now())
            }, f, indent=4, ensure_ascii=False)

        logging.info(f"[{datetime.now()}] Scraping exitoso de {url}")

    except Exception as e:
        logging.error(f"[{datetime.now()}] Error al scrapear {url}: {str(e)}")

if __name__ == "__main__":
    scrape_example()
