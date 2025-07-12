import logging
import os
from typing import Optional

def get_logger(name: Optional[str] = None) -> logging.Logger:
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)

        # Console handler
        stream_handler = logging.StreamHandler()
        stream_formatter = logging.Formatter(
            fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        stream_handler.setFormatter(stream_formatter)
        logger.addHandler(stream_handler)

        # File handler
        file_handler = logging.FileHandler(os.path.join(log_dir, "data_analysis_log.log"), mode='w', encoding='utf-8')
        file_handler.setFormatter(stream_formatter)
        logger.addHandler(file_handler)

        logger.propagate = False

    return logger

