# db_tool/utils.py
import logging
import os
import json
from rich.logging import RichHandler

# Set up rich logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler()]
)

def log_error(error_message):
    logging.error(error_message)

def log_info(info_message):
    logging.info(info_message)

def save_config(config, filename='db_tool/config/config.json'):
    with open(filename, 'w') as f:
        json.dump(config, f)

def load_config(filename='db_tool/config/config.json'):
    with open(filename, 'r') as f:
        return json.load(f)

