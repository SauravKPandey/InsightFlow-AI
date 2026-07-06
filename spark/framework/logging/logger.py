import logging
import os
import sys
from pathlib import Path


def get_logger(
    name: str,
    env_config: dict
) -> logging.Logger:

    logger = logging.getLogger(name)

    # Prevent duplicate handlers
    if logger.handlers:
        return logger

    # ----------------------------
    # Log Level
    # ----------------------------
    log_level = env_config["logging"]["level"].upper()

    logger.setLevel(
        getattr(logging, log_level)
    )

    logger.propagate = False

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    )

    # ----------------------------
    # Console Handler
    # ----------------------------
    if env_config["logging"]["console"]["enabled"]:

        console_handler = logging.StreamHandler(sys.stdout)

        console_handler.setFormatter(formatter)

        logger.addHandler(console_handler)

    # ----------------------------
    # File Handler
    # ----------------------------
    if env_config["logging"]["file"]["enabled"]:

        log_root = Path(
            env_config["logging"]["file"]["path"]
        )

        log_root.mkdir(
            parents=True,
            exist_ok=True
        )

        log_file = log_root / f"{name}.log"

        log_file.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        file_handler = logging.FileHandler(
            log_file,
            mode="a"
        )

        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

    # ----------------------------
    # Future Cloud Logging
    # ----------------------------
    if env_config["logging"]["cloud"]["enabled"]:

        # Placeholder for future GCP Cloud Logging
        #
        # from google.cloud import logging
        #
        # client = logging.Client()
        # handler = CloudLoggingHandler(client)
        # logger.addHandler(handler)

        pass

    return logger