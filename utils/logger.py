import logging
import json

def setup_logger(log_file):
    logger = logging.getLogger("scraper")
    handler = logging.FileHandler(f"./logs/{log_file}")
    formatter = logging.Formatter('%(message)s')
    handler.setFormatter(formatter)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    class JsonLog:
        def info(self, obj): logger.info(json.dumps(obj))
        def error(self, obj): logger.error(json.dumps(obj))

    return JsonLog()
