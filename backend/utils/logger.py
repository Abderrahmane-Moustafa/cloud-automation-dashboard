import logging
from logging.handlers import RotatingFileHandler
import os

# Ensure logs directory exists
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

# Define log file path
log_file = os.path.join(log_dir, "cloud_dashboard.log")

# Configure logging
logger = logging.getLogger("cloud_dashboard_logger")
logger.setLevel(logging.INFO)

# File handler with rotation
handler = RotatingFileHandler(log_file, maxBytes=1_000_000, backupCount=3)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Avoid duplicate handlers
if not logger.hasHandlers():
    logger.addHandler(handler)