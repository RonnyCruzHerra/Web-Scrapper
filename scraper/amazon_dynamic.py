from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from db.db_connection import Session
from db.models import ScrapedData
from datetime import datetime
import time

def scrape_amazon_dynamic(query="laptop", pages=1):
    options = Options()
    options.add_argument("--headless")  # Ejecuta navegador sin interfaz
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    
    # Ruta al navegador Chrome
    options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    
    # Ruta al chromedriver
    service = Service(r"./drivers/chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)

    session = Session()
    scraped_count = 0

    try:
        for page in range(1, pages + 1):
            search_url = f"https://www.amazon.com/s?k={query}&page={page}"
            driver.get(search_url)
            time.sleep(3)  # Puedes reemplazar por WebDriverWait para mejor rendimiento

            results = driver.find_elements(By.CSS_SELECTOR, ".s-result-item[data-asin]")
            for result in results:
                try:
                    # Título dentro del <h2><span>
                    title_el = result.find_element(By.CSS_SELECTOR, "h2 span")
                    title = title_el.text

                    # URL fuera del <h2>, usando clases del <a>
                    url_el = result.find_element(By.CSS_SELECTOR, "a.a-link-normal.s-underline-text.s-underline-link-text.s-link-style.a-text-normal")
                    url = url_el.get_attribute("href")

                    # Precio (puede que no exista)
                    try:
                        content = result.find_element(By.CSS_SELECTOR, ".a-price .a-offscreen").text
                    except:
                        content = "Sin precio"

                    # Guardar en la base de datos
                    scraped = ScrapedData(
                        title=title,
                        url=url,
                        content=content,
                        scraped_at=datetime.utcnow()
                    )
                    session.add(scraped)
                    scraped_count += 1
                except Exception as e:
                    print(f"Error scraping item: {e}")

            session.commit()
    finally:
        session.close()
        driver.quit()

    print(f"Scraping finalizado. Productos guardados: {scraped_count}")
    return scraped_count

if __name__ == "__main__":
    scrape_amazon_dynamic("laptop", 1)
