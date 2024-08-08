import logging
import json
import sys

from ..logger.default_logger import PrintLogger

def import_db_credentials_json(fname, logger=PrintLogger):
    logger.info(f"loading db config file")
    try:
        # Load database config
        with open(fname, 'r') as config_file:
            config = json.load(config_file)
        logger.info(f"db config loaded")
    except Exception as e:
        logger.error(f"Failed to load database configuration: %s", e)
        sys.exit(1)  # Exit the script with a non-zero status code to indicate an error
    
    return config