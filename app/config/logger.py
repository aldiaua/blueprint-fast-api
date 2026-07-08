import logging
import sys

import structlog

logging.basicConfig(
    level=logging.INFO,
    stream=sys.stdout,
    format="%(message)s",
)

structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.processors.JSONRenderer(),
    ],
)

logger = structlog.get_logger()
