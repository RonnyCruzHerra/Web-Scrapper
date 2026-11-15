# Web-Scrapper

<!-- local-development:start -->
## Desarrollo local

Consulta [RUNNING.md](RUNNING.md) para ubicar cada componente, abrirlo en su IDE, compilarlo y conocer las comprobaciones realizadas y los requisitos pendientes.
<!-- local-development:end -->

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

# Día 3 - API Flask + Generación de Selectores con LLM + Manejo de Archivos

## Objetivo

Implementar un API REST usando Flask que exponga servicios para:

- Generar selectores CSS/XPath dinámicos a partir de fragmentos HTML y texto objetivo, mediante un modelo LLM Azure OpenAI.
- Servir archivos JSON exportados de scrapers para consumo en frontend.
- Gestionar peticiones con manejo de errores y buenas prácticas.

---

## 1. Configuración del entorno

- Activar entorno virtual Python si no está activo:

python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate


- Instalar dependencias principales:

pip install -r requirements.txt

- Dependencias claves para este día:

flask

flask-cors

python-dotenv

openai (Azure OpenAI SDK)

werkzeug (para seguridad en nombres de archivo)

## 2. Variables de entorno (.env)
Configurar archivo .env con las siguientes variables para conexión segura a Azure OpenAI y configuración general:

AZURE_OPENAI_ENDPOINT=https://voiceflip-openai.openai.azure.com/
AZURE_OPENAI_KEY=tu_api_key_aqui_sin_espacios_ni_comillas
AZURE_OPENAI_DEPLOYMENT=gpt-4o-mini
AZURE_OPENAI_VERSION=2024-12-01-preview


## 3. Implementación de la API Flask
Archivo principal: main.py para levantar la app Flask.

Módulo api/ con:

__init__.py: fábrica de la app Flask, CORS, registro del blueprint.

routes.py: definición de endpoints:

GET /api/: prueba que la API está activa.

POST /api/generate-selector: recibe JSON con html y target para generar selector con LLM.

GET /api/data/<filename>: sirve JSON desde carpeta data/ con validación y manejo de errores.

Módulo ilm/selector_generator.py: conexión con Azure OpenAI para generar selector dinámico usando prompt contextualizado.

## 4. Uso y pruebas
Levantar servidor:

python main.py
Probar endpoint raíz:

curl http://127.0.0.1:5000/api/
Probar generación selector:

curl -X POST http://127.0.0.1:5000/api/generate-selector \
  -H "Content-Type: application/json" \
  -d '{"html": "<div>Hola Mundo</div>", "target": "Hola Mundo"}'
Probar servir archivo JSON (ejemplo):

curl http://127.0.0.1:5000/api/data/ejemplo.json

## 5. Manejo de errores y seguridad
Validación de inputs en endpoints con respuestas claras y códigos HTTP apropiados (400, 404, 500).

Validación de nombres de archivos con werkzeug.utils.secure_filename para evitar path traversal.

Captura y reporte de excepciones en conexión con Azure OpenAI.

## 6. Estructura del proyecto Día 3 (parcial)

api/
  __init__.py
  routes.py
ilm/
  selector_generator.py
data/
  ejemplo.json
main.py
.env
requirements.txt
README.md


# Día 4 – Frontend y Visualización con Calendar.js

## Objetivo del día
Implementar una interfaz gráfica moderna y funcional que visualice los datos scrapeados mediante un dashboard y calendario interactivo.

---

## Avances realizados

- Se creó la carpeta `frontend/` con los siguientes archivos:
  - `index.html`: interfaz principal del dashboard
  - `styles.css`: estilos base para layout y modal
  - `calendar.js`: lógica JS para renderizar y alimentar FullCalendar.js

- Se configuró FullCalendar.js desde CDN (`v6.1.11`) con idioma español y vista mensual.

- Se conectó el calendario con el endpoint de backend `/api/scraped-data` para visualizar los eventos almacenados.

- Se agregó una verificación: si no hay eventos válidos, se muestran eventos de prueba por defecto.

- Se implementó un modal interactivo para ver detalles completos del scraping al hacer clic sobre un evento.

---

## Archivos claves
frontend/
├── index.html
├── styles.css
└── scripts/
└── calendar.js


---

## Consideraciones técnicas

- Se usó `defer` en la carga de scripts para evitar errores por falta de definición de `FullCalendar`.
- Se configuró `locale: 'es'` para mostrar el calendario en español.
- Las rutas estáticas se sirvieron correctamente desde Flask con `/api/static/...`
- El calendario se adapta dinámicamente según los datos disponibles en la API.

---

## Próximo paso (Día 5)

Atomatización del Scraping 
Este sistema implementa la automatización de tareas programadas usando **APScheduler** para ejecutar scraping, respaldos y limpieza de archivos de forma continua y sin intervención manual.

Se realizo:
Scraping Estático:Ejecuta el módulo de scraping estático (`StaticScraper`) o un scraping de respaldo básico. 
Scraping Dinámico: Ejecuta el módulo `DynamicScraper` o, en su defecto, un scraping básico con `requests` y `BeautifulSoup`. 
Respaldo de la Base de Datos: Genera un `.sql` de respaldo con `pg_dump` en la carpeta `./data/`. 
Limpieza de Datos Antiguos :Borra logs y archivos descargados con más de `X` días de antigüedad (según configuración). 

scheduler.py contiene:

- Clase `ScrapingScheduler`: encargada de configurar el planificador y ejecutar las tareas.
- Funciones auxiliares: para scraping, backup y limpieza.
- Registro de resultados en:
  - `./logs/scheduler.log` (texto plano)
  - `./logs/scheduler_executions.json` (formato estructurado JSON)
 
    Variables de Entorno .env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=scraping_db
DB_USER=postgres
DB_PASSWORD=admin
SCRAPING_INTERVAL=60         
BACKUP_HOUR=2                
CLEANUP_DAYS=30

Dependencias necesarias:
APScheduler
psycopg2-binary==2.8.6
SQLAlchemy
python-dotenv
requests
beautifulsoup4
