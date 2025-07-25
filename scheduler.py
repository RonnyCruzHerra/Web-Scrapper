#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Automatización para Plataforma de Scraping
Día 5 - Automatización con APScheduler
Autor: [Roiner Duran]
Fecha: 2025
"""

import os
import sys
import json
import logging
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

try:
    from apscheduler.schedulers.blocking import BlockingScheduler
    from apscheduler.triggers.cron import CronTrigger
    from apscheduler.triggers.interval import IntervalTrigger
    from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
    from apscheduler.executors.pool import ThreadPoolExecutor
except ImportError as e:
    print(f"Error: APScheduler no está instalado. Ejecuta: pip install APScheduler")
    sys.exit(1)

try:
    import psycopg2
    from sqlalchemy import create_engine
except ImportError as e:
    print(f"Error: PostgreSQL libraries no están instaladas. Ejecuta: pip install psycopg2-binary sqlalchemy")
    sys.exit(1)

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('./logs/scheduler.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# --- FUNCIONES LIBRES PARA LOS JOBS ---

def run_static_scraping_job(config):
    scheduler = ScrapingScheduler(config)
    scheduler.run_static_scraping()

def run_dynamic_scraping_job(config):
    scheduler = ScrapingScheduler(config)
    scheduler.run_dynamic_scraping()

def backup_database_job(config):
    scheduler = ScrapingScheduler(config)
    scheduler.backup_database()

def cleanup_old_data_job(config):
    scheduler = ScrapingScheduler(config)
    scheduler.cleanup_old_data()

class ScrapingScheduler:
    """
    Clase principal para la automatización de tareas de scraping
    """

    def __init__(self, config=None):
        self.scheduler = None
        self.config = config if config else self.load_config()
        self.db_url = f"postgresql://{self.config['db_user']}:{self.config['db_password']}@{self.config['db_host']}:{self.config['db_port']}/{self.config['db_name']}"
        self.setup_scheduler()

    def load_config(self):
        """Carga configuración desde variables de entorno"""
        return {
            'db_host': os.getenv('DB_HOST', 'localhost'),
            'db_port': os.getenv('DB_PORT', '5432'),
            'db_name': os.getenv('DB_NAME', 'scraping_db'),
            'db_user': os.getenv('DB_USER', 'postgres'),
            'db_password': os.getenv('DB_PASSWORD', 'password'),
            'scraping_interval': int(os.getenv('SCRAPING_INTERVAL', '60')),  # minutos
            'backup_hour': int(os.getenv('BACKUP_HOUR', '2')),  # hora del día
            'cleanup_days': int(os.getenv('CLEANUP_DAYS', '30'))  # días de retención
        }

    def setup_scheduler(self):
        """Configura el scheduler con base de datos y ejecutores"""
        try:
            jobstores = {
                'default': SQLAlchemyJobStore(url=self.db_url, tablename='scheduled_jobs')
            }
            executors = {
                'default': ThreadPoolExecutor(max_workers=4),
            }
            job_defaults = {
                'coalesce': False,
                'max_instances': 3,
                'misfire_grace_time': 30
            }
            self.scheduler = BlockingScheduler(
                jobstores=jobstores,
                executors=executors,
                job_defaults=job_defaults,
                timezone='America/Costa_Rica'
            )
            logger.info("Scheduler configurado correctamente")
        except Exception as e:
            logger.error(f"Error configurando scheduler: {e}")
            raise

    def run_static_scraping(self):
        """Ejecuta scraping estático"""
        try:
            logger.info("Iniciando scraping estático programado")
            try:
                sys.path.append('./scraper')
                from scraper.static_scraper import StaticScraper
                scraper = StaticScraper()
                results = scraper.scrape_all_sites()
            except ImportError:
                logger.warning("StaticScraper no encontrado, usando scraping básico")
                results = self.basic_scraping_example()
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'type': 'static_scraping',
                'status': 'success',
                'records_scraped': len(results) if results else 0,
                'execution_time': datetime.now().isoformat()
            }
            self.log_execution(log_entry)
            logger.info(f"Scraping estático completado: {len(results) if results else 0} registros")
            return results
        except Exception as e:
            logger.error(f"Error en scraping estático: {e}")
            error_log = {
                'timestamp': datetime.now().isoformat(),
                'type': 'static_scraping',
                'status': 'error',
                'error_message': str(e)
            }
            self.log_execution(error_log)
            return []

    def basic_scraping_example(self):
        """Scraping básico de ejemplo cuando no existen los módulos principales"""
        try:
            import requests
            from bs4 import BeautifulSoup
            url = "https://httpbin.org/html"
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            title = soup.find('h1')
            results = [{
                'url': url,
                'title': title.text if title else 'Sin título',
                'timestamp': datetime.now().isoformat(),
                'status': 'success'
            }]
            return results
        except Exception as e:
            logger.error(f"Error en scraping básico: {e}")
            return []

    def run_dynamic_scraping(self):
        """Ejecuta scraping dinámico"""
        try:
            logger.info("Iniciando scraping dinámico programado")
            try:
                sys.path.append('./scraper')
                from scraper.dynamic_scraper import DynamicScraper
                scraper = DynamicScraper()
                results = scraper.scrape_dynamic_content()
            except ImportError:
                logger.warning("DynamicScraper no encontrado, usando scraping básico")
                results = self.basic_scraping_example()
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'type': 'dynamic_scraping',
                'status': 'success',
                'records_scraped': len(results) if results else 0,
                'execution_time': datetime.now().isoformat()
            }
            self.log_execution(log_entry)
            logger.info(f"Scraping dinámico completado: {len(results) if results else 0} registros")
            return results
        except Exception as e:
            logger.error(f"Error en scraping dinámico: {e}")
            error_log = {
                'timestamp': datetime.now().isoformat(),
                'type': 'dynamic_scraping',
                'status': 'error',
                'error_message': str(e)
            }
            self.log_execution(error_log)
            return []

    def backup_database(self):
        """Realiza backup de la base de datos"""
        try:
            logger.info("Iniciando backup de base de datos")
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_file = f"./data/backup_scraping_db_{timestamp}.sql"
            backup_command = f"""pg_dump -h {self.config['db_host']} -p {self.config['db_port']} -U {self.config['db_user']} -d {self.config['db_name']} > {backup_file}"""
            os.system(backup_command)
            if os.path.exists(backup_file):
                file_size = os.path.getsize(backup_file)
                logger.info(f"Backup completado: {backup_file} ({file_size} bytes)")
                log_entry = {
                    'timestamp': datetime.now().isoformat(),
                    'type': 'database_backup',
                    'status': 'success',
                    'backup_file': backup_file,
                    'file_size': file_size
                }
                self.log_execution(log_entry)
            else:
                raise Exception("Archivo de backup no se creó")
        except Exception as e:
            logger.error(f"Error en backup de base de datos: {e}")
            error_log = {
                'timestamp': datetime.now().isoformat(),
                'type': 'database_backup',
                'status': 'error',
                'error_message': str(e)
            }
            self.log_execution(error_log)
            raise

    def cleanup_old_data(self):
        """Limpia datos antiguos según configuración"""
        try:
            logger.info("Iniciando limpieza de datos antiguos")
            conn = psycopg2.connect(self.db_url)
            cursor = conn.cursor()
            cleanup_date = datetime.now() - timedelta(days=self.config['cleanup_days'])
            cursor.execute("""
                DELETE FROM scraping_logs 
                WHERE created_at < %s
            """, (cleanup_date,))
            deleted_logs = cursor.rowcount
            downloads_path = './downloads'
            deleted_files = 0
            if os.path.exists(downloads_path):
                for filename in os.listdir(downloads_path):
                    file_path = os.path.join(downloads_path, filename)
                    if os.path.isfile(file_path):
                        file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                        if file_time < cleanup_date:
                            os.remove(file_path)
                            deleted_files += 1
            conn.commit()
            conn.close()
            logger.info(f"Limpieza completada: {deleted_logs} logs, {deleted_files} archivos")
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'type': 'data_cleanup',
                'status': 'success',
                'deleted_logs': deleted_logs,
                'deleted_files': deleted_files
            }
            self.log_execution(log_entry)
        except Exception as e:
            logger.error(f"Error en limpieza de datos: {e}")
            error_log = {
                'timestamp': datetime.now().isoformat(),
                'type': 'data_cleanup',
                'status': 'error',
                'error_message': str(e)
            }
            self.log_execution(error_log)
            raise

    def log_execution(self, log_entry):
        """Registra la ejecución de tareas en archivo JSON"""
        try:
            log_file = './logs/scheduler_executions.json'
            if os.path.exists(log_file):
                with open(log_file, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
            else:
                logs = []
            logs.append(log_entry)
            with open(log_file, 'w', encoding='utf-8') as f:
                json.dump(logs, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error registrando ejecución: {e}")

    def add_jobs(self):
        """Agrega trabajos programados al scheduler"""
        try:
            config = self.config
            self.scheduler.add_job(
                func=run_static_scraping_job,
                args=[config],
                trigger=IntervalTrigger(minutes=config['scraping_interval']),
                id='static_scraping',
                name='Scraping Estático Programado',
                replace_existing=True
            )
            self.scheduler.add_job(
                func=run_dynamic_scraping_job,
                args=[config],
                trigger=IntervalTrigger(hours=2),
                id='dynamic_scraping',
                name='Scraping Dinámico Programado',
                replace_existing=True
            )
            self.scheduler.add_job(
                func=backup_database_job,
                args=[config],
                trigger=CronTrigger(hour=config['backup_hour'], minute=0),
                id='daily_backup',
                name='Backup Diario de Base de Datos',
                replace_existing=True
            )
            self.scheduler.add_job(
                func=cleanup_old_data_job,
                args=[config],
                trigger=CronTrigger(day_of_week=0, hour=3, minute=0),
                id='weekly_cleanup',
                name='Limpieza Semanal de Datos',
                replace_existing=True
            )
            logger.info("Trabajos programados agregados correctamente")
        except Exception as e:
            logger.error(f"Error agregando trabajos: {e}")
            raise

    def start(self):
        """Inicia el scheduler"""
        try:
            logger.info("Iniciando sistema de automatización...")
            self.add_jobs()
            jobs = self.scheduler.get_jobs()
            logger.info(f"Trabajos programados ({len(jobs)}):")
            for job in jobs:
                next_run = getattr(job, "next_run_time", None)
                logger.info(f"  - {job.name} (ID: {job.id}) - Próxima ejecución: {next_run}")
            logger.info("Scheduler iniciado. Presiona Ctrl+C para detener.")
            self.scheduler.start()
        except KeyboardInterrupt:
            logger.info("Deteniendo scheduler...")
            self.scheduler.shutdown()
            logger.info("Scheduler detenido correctamente")
        except Exception as e:
            logger.error(f"Error en scheduler: {e}")
            raise

def main():
    """Función principal"""
    try:
        os.makedirs('./logs', exist_ok=True)
        os.makedirs('./data', exist_ok=True)
        os.makedirs('./downloads', exist_ok=True)
        scheduler = ScrapingScheduler()
        scheduler.start()
    except Exception as e:
        logger.error(f"Error crítico: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
