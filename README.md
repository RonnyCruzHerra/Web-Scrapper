# Web-Scrapper

# Plataforma de Scraping Inteligente

Este proyecto implementa un sistema modular para scraping web estático y dinámico, persistencia en PostgreSQL, API REST con Flask, y visualización en un dashboard moderno. Desarrollado como práctica profesional de Ingeniería en Tecnologías de la Información.

## Día 1: Scraping estático

- Se conectó a `https://example.com`
- Se almacenó el título y el contenido en PostgreSQL
- Se generó un archivo JSON de respaldo

# Día 2 - Scraping Dinámico con Selenium + Persistencia en PostgreSQL

## Objetivo

Implementar un scraper dinámico usando Selenium para extraer datos de páginas web que cargan contenido mediante JavaScript, y almacenar la información en PostgreSQL con manejo robusto de inserciones y actualizaciones.

---

## 1. Configuración del entorno

- Entorno virtual Python:
  ```bash
  python -m venv .venv
  .venv\Scripts\activate  # Windows
  source .venv/bin/activate  # Linux/Mac

### 1.1. Instalación de dependencias:

- pip install -r requirements.txt

### 1.2. Dependencias relevantes para el día:

selenium==4.11.2

psycopg2-binary (versión 2.8.6 por compatibilidad y evitar errores de compilación)

python-dotenv para gestión segura de variables de entorno

## 2. Scraping dinámico con Selenium
- Uso de Selenium para abrir un navegador Chromium (Chrome o Brave) con WebDriver.

- Ejemplo básico de apertura, extracción y cierre en scraper/dynamic_scraper.py.
- Control de tiempos de espera para carga dinámica mediante WebDriverWait.

## 3. Persistencia en PostgreSQL
- Conexión a base de datos configurada con .env:

DB_NAME=webdata
DB_USER=postgres
DB_PASSWORD=admin
DB_HOST=localhost
DB_PORT=5432


- Tabla scraped_data con estructura:

CREATE TABLE IF NOT EXISTS scraped_data (
    id SERIAL PRIMARY KEY,
    title TEXT,
    url TEXT UNIQUE,
    content TEXT,
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
- Inserción con manejo de conflictos para evitar duplicados:

cur.execute("""
    INSERT INTO scraped_data (title, url, content)
    VALUES (%s, %s, %s)
    ON CONFLICT (url) DO UPDATE SET content = EXCLUDED.content
""", (title, url, content))

## 4. Pruebas y verificación
- Uso de script de prueba prueba_insert.py para verificar inserción y actualización.

- Comandos útiles en psql para confirmar datos:
SELECT * FROM scraped_data ORDER BY scraped_at DESC LIMIT 5;
\d scraped_data
Manejo de excepciones y errores mediante bloques try-except para evitar caídas en ejecución.

## 5. Estructura del proyecto (parcial)

/scraper
  /dynamic_scraper.py
/db
  /db_connection.py
prueba_insert.py
requirements.txt
.env
README_dia2.md
## 6. Consejos técnicos y buenas prácticas
- Mantener variables sensibles fuera del código con .env.

- Usar ON CONFLICT para evitar errores por duplicados.

- Controlar cierres de conexiones y cursores para evitar fugas.

- Evitar instalación de psycopg2-binary en versiones incompatibles; preferir la 2.8.6 para Windows.

- Usar logs estructurados (en futuros días) para mejor depuración.

- Confirmar siempre resultados con consultas SQL directas.


