import logging
from logging.handlers import TimedRotatingFileHandler
import os
import sys
import structlog

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "app.log")

os.makedirs(LOG_DIR, exist_ok=True)

file_handler = TimedRotatingFileHandler(
    filename=LOG_FILE,
    when="midnight",
    interval=1,
    backupCount=30,
    encoding="utf-8",
)

file_handler.suffix = "%Y-%m-%d"
file_handler.setFormatter(logging.Formatter("%(message)s"))

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(logging.Formatter("%(message)s"))

json_logger = logging.getLogger("AppJsonLogger")
json_logger.setLevel([logging.INFO, logging.DEBUG, logging.ERROR][0])  # Ubah level log sesuai kebutuhan
json_logger.addHandler(file_handler)
json_logger.addHandler(console_handler)
json_logger.propagate = False

logging.basicConfig(
    level=logging.WARNING,
    handlers=[logging.NullHandler()]
)

structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.processors.JSONRenderer(),
    ],
    logger_factory=lambda: json_logger,
)

logger = structlog.get_logger()