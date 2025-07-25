from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def scrape_dynamic(url):
    options = Options()
    # Comenta la línea siguiente si quieres usar Chrome normal
    options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

    service = Service(r"./drivers/chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(url)
        time.sleep(3)  # Esperar carga (puedes mejorar con waits explícitos)

        title = driver.title
        current_url = driver.current_url
        # Extrae contenido completo del body como ejemplo
        content = driver.find_element(By.TAG_NAME, "body").text

        return {
            "title": title,
            "url": current_url,
            "content": content
        }
    except Exception as e:
        print(f"Error durante scraping dinámico: {e}")
        return None
    finally:
        driver.quit()
