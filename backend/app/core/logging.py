import logging
import sys
from datetime import datetime, timezone


class StructuredFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        timestamp = datetime.now(timezone.utc).isoformat()
        log_entry = {
            "timestamp": timestamp,
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
        
        # Return clean structured log representation
        return f"[{timestamp}] [{record.levelname:^7}] [{record.name}]: {record.getMessage()}"


def setup_logging(level: str = "INFO") -> None:
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, level.upper(), logging.INFO))

    # Remove existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(StructuredFormatter())
    root_logger.addHandler(console_handler)

    # Suppress verbose third-party loggers
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("asyncpg").setLevel(logging.WARNING)
